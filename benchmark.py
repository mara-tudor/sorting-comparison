"""
benchmark.py
============
Benchmarks all seven sorting algorithms across five input distributions
and multiple array sizes. Results are saved to results/results.csv.

Usage:
    python benchmark.py

Requirements:
    Python 3.8+  (no external libraries needed for benchmarking)
    matplotlib   (only needed for --plot flag)

    pip install matplotlib
"""

import time
import random
import csv
import os
import sys
import copy

from algorithms import ALL_ALGORITHMS

# ── Configuration ────────────────────────────────────────────────────────────

# Sizes to test for O(n log n) algorithms
SIZES_FAST = [100, 500, 1_000, 5_000, 10_000, 50_000, 100_000]

# O(n^2) algorithms are slow — limit their maximum size
SIZES_SLOW = [100, 500, 1_000, 5_000, 10_000]

SLOW_ALGORITHMS = {"Insertion Sort", "Selection Sort", "Bubble Sort"}

DISTRIBUTIONS = ["random", "sorted", "reverse", "nearly_sorted", "constant"]

TRIALS = 15       # number of repetitions per (algorithm, size, distribution)
SEED   = 42       # for reproducibility

# ── Input generators ─────────────────────────────────────────────────────────

def generate_input(distribution: str, n: int, rng: random.Random) -> list:
    if distribution == "random":
        return [rng.randint(1, 10 * n) for _ in range(n)]
    elif distribution == "sorted":
        return list(range(1, n + 1))
    elif distribution == "reverse":
        return list(range(n, 0, -1))
    elif distribution == "nearly_sorted":
        a = list(range(1, n + 1))
        swaps = max(1, int(n ** 0.5))
        for _ in range(swaps):
            i = rng.randint(0, n - 2)
            a[i], a[i + 1] = a[i + 1], a[i]
        return a
    elif distribution == "constant":
        return [1] * n
    else:
        raise ValueError(f"Unknown distribution: {distribution}")

# ── Timing helper ─────────────────────────────────────────────────────────────

def time_sort(func, arr) -> float:
    """Return wall-clock time in seconds to sort arr using func."""
    data = arr[:]          # ensure each trial gets the same input
    start = time.perf_counter()
    func(data)
    return time.perf_counter() - start

# ── Correctness check ─────────────────────────────────────────────────────────

def verify_all(n: int = 200):
    """Quick sanity-check: every algorithm must produce a sorted output."""
    rng = random.Random(0)
    arr = [rng.randint(1, 1000) for _ in range(n)]
    expected = sorted(arr)
    for name, func in ALL_ALGORITHMS.items():
        result = func(arr[:])
        assert result == expected, f"{name} produced wrong output!"
    print("✓ All algorithms passed correctness check.\n")

# ── Main benchmark ────────────────────────────────────────────────────────────

def run_benchmark():
    verify_all()

    os.makedirs("results", exist_ok=True)
    csv_path = os.path.join("results", "results.csv")

    fieldnames = ["algorithm", "distribution", "n", "trial", "time_s"]

    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for name, func in ALL_ALGORITHMS.items():
            sizes = SIZES_SLOW if name in SLOW_ALGORITHMS else SIZES_FAST
            for dist in DISTRIBUTIONS:
                for n in sizes:
                    rng = random.Random(SEED)
                    times = []
                    for trial in range(TRIALS):
                        arr = generate_input(dist, n, rng)
                        t = time_sort(func, arr)
                        times.append(t)
                        writer.writerow({
                            "algorithm":    name,
                            "distribution": dist,
                            "n":            n,
                            "trial":        trial,
                            "time_s":       round(t, 6),
                        })

                    mean_t = sum(times) / len(times)
                    print(
                        f"{name:20s} | {dist:14s} | n={n:>7,} | "
                        f"mean={mean_t:.4f}s"
                    )

    print(f"\n✓ Results saved to {csv_path}")
    return csv_path

# ── Optional plotting ─────────────────────────────────────────────────────────

def plot_results(csv_path: str):
    try:
        import matplotlib.pyplot as plt
        import collections
    except ImportError:
        print("matplotlib not installed — skipping plots.")
        print("Install with:  pip install matplotlib")
        return

    # Read CSV
    data = collections.defaultdict(lambda: collections.defaultdict(dict))
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        raw = list(reader)

    # Compute means per (algorithm, distribution, n)
    from itertools import groupby
    keyfn = lambda r: (r["algorithm"], r["distribution"], int(r["n"]))
    raw.sort(key=keyfn)
    means = {}
    for key, rows in groupby(raw, key=keyfn):
        ts = [float(r["time_s"]) for r in rows]
        means[key] = sum(ts) / len(ts)

    os.makedirs("plots", exist_ok=True)

    # Plot 1: random distribution, all algorithms
    fig, ax = plt.subplots(figsize=(9, 5))
    for name in ALL_ALGORITHMS:
        sizes = SIZES_SLOW if name in SLOW_ALGORITHMS else SIZES_FAST
        ys = [means.get((name, "random", n), None) for n in sizes]
        xs = [s for s, y in zip(sizes, ys) if y is not None]
        ys = [y for y in ys if y is not None]
        ax.plot(xs, ys, marker="o", label=name)

    ax.set_xlabel("Array size (n)")
    ax.set_ylabel("Time (seconds)")
    ax.set_title("Sorting algorithms — random input")
    ax.legend(fontsize=8)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.grid(True, which="both", linestyle="--", alpha=0.4)
    fig.tight_layout()
    path1 = os.path.join("plots", "random_all.png")
    fig.savefig(path1, dpi=150)
    print(f"  Saved {path1}")
    plt.close(fig)

    # Plot 2: fast algorithms across all distributions at n=10,000
    n_target = 10_000
    fast_algos = [a for a in ALL_ALGORITHMS if a not in SLOW_ALGORITHMS]
    fig, ax = plt.subplots(figsize=(9, 5))
    x = range(len(DISTRIBUTIONS))
    width = 0.12
    for i, name in enumerate(fast_algos):
        ys = [means.get((name, d, n_target), 0) for d in DISTRIBUTIONS]
        offset = (i - len(fast_algos) / 2) * width
        ax.bar([xi + offset for xi in x], ys, width, label=name)

    ax.set_xticks(list(x))
    ax.set_xticklabels(DISTRIBUTIONS)
    ax.set_ylabel("Time (seconds)")
    ax.set_title(f"Fast algorithms across distributions (n={n_target:,})")
    ax.legend(fontsize=8)
    ax.grid(True, axis="y", linestyle="--", alpha=0.4)
    fig.tight_layout()
    path2 = os.path.join("plots", "distributions_fast.png")
    fig.savefig(path2, dpi=150)
    print(f"  Saved {path2}")
    plt.close(fig)

    print("✓ Plots saved to plots/")

# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    csv_path = run_benchmark()
    if "--plot" in sys.argv:
        print("\nGenerating plots...")
        plot_results(csv_path)
