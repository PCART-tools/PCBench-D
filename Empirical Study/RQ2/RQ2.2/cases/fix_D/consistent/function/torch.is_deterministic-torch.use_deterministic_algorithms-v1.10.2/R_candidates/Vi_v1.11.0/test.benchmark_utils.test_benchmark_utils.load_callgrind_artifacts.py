def load_callgrind_artifacts() -> Tuple[benchmark_utils.CallgrindStats, benchmark_utils.CallgrindStats]:
    """Hermetic artifact to unit test Callgrind wrapper.

    In addition to collecting counts, this wrapper provides some facilities for
    manipulating and displaying the collected counts. The results of several
    measurements are stored in callgrind_artifacts.json.

    While FunctionCounts and CallgrindStats are pickleable, the artifacts for
    testing are stored in raw string form for easier inspection and to avoid
    baking any implementation details into the artifact itself.
    """
    with open(CALLGRIND_ARTIFACTS, "rt") as f:
        artifacts = json.load(f)

    pattern = re.compile(r"^\s*([0-9]+)\s(.+)$")

    def to_function_counts(
        count_strings: List[str],
        inclusive: bool
    ) -> benchmark_utils.FunctionCounts:
        data: List[benchmark_utils.FunctionCount] = []
        for cs in count_strings:
            # Storing entries as f"{c} {fn}" rather than [c, fn] adds some work
            # reviving the artifact, but it makes the json much easier to read.
            match = pattern.search(cs)
            assert match is not None
            c, fn = match.groups()
            data.append(benchmark_utils.FunctionCount(count=int(c), function=fn))

        return benchmark_utils.FunctionCounts(
            tuple(sorted(data, reverse=True)),
            inclusive=inclusive)

    baseline_inclusive = to_function_counts(artifacts["baseline_inclusive"], True)
    baseline_exclusive = to_function_counts(artifacts["baseline_exclusive"], False)

    stats_no_data = benchmark_utils.CallgrindStats(
        benchmark_utils.TaskSpec("y = torch.ones(())", "pass"),
        number_per_run=1000,
        built_with_debug_symbols=True,
        baseline_inclusive_stats=baseline_inclusive,
        baseline_exclusive_stats=baseline_exclusive,
        stmt_inclusive_stats=to_function_counts(artifacts["ones_no_data_inclusive"], True),
        stmt_exclusive_stats=to_function_counts(artifacts["ones_no_data_exclusive"], False),
        stmt_callgrind_out=None,
    )

    stats_with_data = benchmark_utils.CallgrindStats(
        benchmark_utils.TaskSpec("y = torch.ones((1,))", "pass"),
        number_per_run=1000,
        built_with_debug_symbols=True,
        baseline_inclusive_stats=baseline_inclusive,
        baseline_exclusive_stats=baseline_exclusive,
        stmt_inclusive_stats=to_function_counts(artifacts["ones_with_data_inclusive"], True),
        stmt_exclusive_stats=to_function_counts(artifacts["ones_with_data_exclusive"], False),
        stmt_callgrind_out=None,
    )

    return stats_no_data, stats_with_data
