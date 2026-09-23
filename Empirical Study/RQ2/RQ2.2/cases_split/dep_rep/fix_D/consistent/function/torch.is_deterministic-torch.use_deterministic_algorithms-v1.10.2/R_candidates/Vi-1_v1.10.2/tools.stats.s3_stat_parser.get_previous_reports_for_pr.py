def get_previous_reports_for_pr(pr: str, ci_job_prefix: str = "") -> List[Tuple[Report, str]]:
    reports: List[Tuple[Report, str]] = []
    logger.info(f'Grabbing reports from PR: {[pr]}')
    summaries = get_test_stats_summaries_for_pr(pr=pr, job_prefix=ci_job_prefix)
    for _, summary in summaries.items():
        reports.extend(summary)
    # sort by summary_timestamp
    reports.sort(reverse=True, key=lambda s: s[1])
    return reports
