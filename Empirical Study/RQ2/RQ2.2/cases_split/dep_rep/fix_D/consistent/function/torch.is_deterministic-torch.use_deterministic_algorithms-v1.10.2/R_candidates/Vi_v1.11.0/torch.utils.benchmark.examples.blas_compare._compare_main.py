def _compare_main():
    results = []
    with open(RESULT_FILE, "rb") as f:
        while True:
            try:
                results.extend(pickle.load(f))
            except EOFError:
                break

    from torch.utils.benchmark import Compare

    comparison = Compare(results)
    comparison.trim_significant_figures()
    comparison.colorize()
    comparison.print()
