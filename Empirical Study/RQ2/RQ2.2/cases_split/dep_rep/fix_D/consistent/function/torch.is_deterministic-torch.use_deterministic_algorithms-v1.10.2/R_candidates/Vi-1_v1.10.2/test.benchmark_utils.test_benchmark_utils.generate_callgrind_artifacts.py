def generate_callgrind_artifacts() -> None:
    """Regenerate `callgrind_artifacts.json`

    Unlike the expect tests, regenerating callgrind counts will produce a
    large diff since build directories and conda/pip directories are included
    in the instruction string. It is also not 100% deterministic (due to jitter
    from Python) and takes over a minute to run. As a result, running this
    function is manual.
    """
    print("Regenerating callgrind artifact.")

    stats_no_data = benchmark_utils.Timer(
        "y = torch.ones(())"
    ).collect_callgrind(number=1000)

    stats_with_data = benchmark_utils.Timer(
        "y = torch.ones((1,))"
    ).collect_callgrind(number=1000)

    user = os.getenv("USER")

    def to_entry(fn_counts):
        return [f"{c} {fn.replace(f'/{user}/', '/test_user/')}" for c, fn in fn_counts]

    artifacts = {
        "baseline_inclusive": to_entry(stats_no_data.baseline_inclusive_stats),
        "baseline_exclusive": to_entry(stats_no_data.baseline_exclusive_stats),
        "ones_no_data_inclusive": to_entry(stats_no_data.stmt_inclusive_stats),
        "ones_no_data_exclusive": to_entry(stats_no_data.stmt_exclusive_stats),
        "ones_with_data_inclusive": to_entry(stats_with_data.stmt_inclusive_stats),
        "ones_with_data_exclusive": to_entry(stats_with_data.stmt_exclusive_stats),
    }

    with open(CALLGRIND_ARTIFACTS, "wt") as f:
        json.dump(artifacts, f, indent=4)
