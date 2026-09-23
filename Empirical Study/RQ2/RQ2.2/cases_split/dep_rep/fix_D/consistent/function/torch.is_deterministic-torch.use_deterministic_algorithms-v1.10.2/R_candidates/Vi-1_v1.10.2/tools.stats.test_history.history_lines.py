def history_lines(
    *,
    commits: List[Tuple[str, datetime]],
    jobs: Optional[List[str]],
    filename: Optional[str],
    suite_name: Optional[str],
    test_name: str,
    delta: int,
    sha_length: int,
    mode: str,
    digits: int,
) -> Iterator[str]:
    prev_time = datetime.now(tz=timezone.utc)
    for sha, time in commits:
        if (prev_time - time).total_seconds() < delta * 3600:
            continue
        prev_time = time
        if jobs is None:
            summaries = get_test_stats_summaries(sha=sha)
        else:
            summaries = get_test_stats_summaries(sha=sha, jobs=jobs)
        if mode == 'columns':
            assert jobs is not None
            # we assume that get_test_stats_summaries here doesn't
            # return empty lists
            omitted = {
                job: len(l) - 1
                for job, l in summaries.items()
                if len(l) > 1
            }
            lines = [make_columns(
                jobs=jobs,
                jsons={job: l[0] for job, l in summaries.items()},
                omitted=omitted,
                filename=filename,
                suite_name=suite_name,
                test_name=test_name,
                digits=digits,
            )]
        else:
            assert mode == 'multiline'
            lines = make_lines(
                jobs=set(jobs or []),
                jsons=summaries,
                filename=filename,
                suite_name=suite_name,
                test_name=test_name,
            )
        for line in lines:
            yield f"{time:%Y-%m-%d %H:%M:%S}Z {sha[:sha_length]} {line}".rstrip()
