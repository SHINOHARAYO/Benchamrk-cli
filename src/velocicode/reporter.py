def print_table(results):
    """
    Prints the benchmark results in a formatted table.
    results: list of dicts with keys: language, benchmark, mean, min, max
    """
    if not results:
        print("No results to display.")
        return

    headers = ["Benchmark", "Language", "Mean (s)", "Min (s)", "Max (s)"]
    # calculate widths
    widths = [len(h) for h in headers]
    for r in results:
        widths[0] = max(widths[0], len(r['benchmark']))
        widths[1] = max(widths[1], len(r['language']))
        widths[2] = max(widths[2], len(f"{r['mean']:.4f}"))
        widths[3] = max(widths[3], len(f"{r['min']:.4f}"))
        widths[4] = max(widths[4], len(f"{r['max']:.4f}"))

    # create format string
    fmt = " | ".join(f"{{:<{w}}}" for w in widths)
    separator = "-+-".join("-" * w for w in widths)

    print(fmt.format(*headers))
    print(separator)

    for r in results:
        print(fmt.format(
            r['benchmark'],
            r['language'],
            f"{r['mean']:.4f}",
            f"{r['min']:.4f}",
            f"{r['max']:.4f}"
        ))
