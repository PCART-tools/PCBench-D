def regression_info(
    *,
    head_sha: Commit,
    head_report: Report,
    base_reports: Dict[Commit, List[Report]],
    job_name: str,
    on_master: bool,
    ancestry_path: int,
    other_ancestors: int,
) -> str:
    """
    Return a human-readable report describing any test time regressions.

    The head_sha and head_report args give info about the current commit
    and its test times. Since Python dicts maintain insertion order
    (guaranteed as part of the language spec since 3.7), the
    base_reports argument must list the head's several most recent
    master commits, from newest to oldest (so the merge-base is
    list(base_reports)[0]).
    """
    simpler_head = simplify(head_report)
    simpler_base: Dict[Commit, List[SimplerReport]] = {}
    for commit, reports in base_reports.items():
        simpler_base[commit] = [simplify(r) for r in reports]
    analysis = analyze(
        head_report=simpler_head,
        base_reports=simpler_base,
    )

    return '\n'.join([
        unlines([
            '----- Historic stats comparison result ------',
            '',
            f'    job: {job_name}',
            f'    commit: {head_sha}',
        ]),

        # don't print anomalies, because sometimes due to sharding, the
        # output from this would be very long and obscure better signal

        # anomalies(analysis),

        graph(
            head_sha=head_sha,
            head_seconds=head_report['total_seconds'],
            base_seconds={
                c: [r['total_seconds'] for r in rs]
                for c, rs in base_reports.items()
            },
            on_master=on_master,
            ancestry_path=ancestry_path,
            other_ancestors=other_ancestors,
        ),
        summary(analysis),
    ])
