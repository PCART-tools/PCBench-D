def get_test_stats_summaries_for_pr(*, pr: str, job_prefix: str) -> Dict[str, List[Tuple[Report, str]]]:
    bucket = get_S3_bucket_readonly(OSSCI_METRICS_BUCKET)
    summaries = bucket.objects.filter(Prefix=f"pr_test_time/{pr}/")
    return _parse_pr_summaries(summaries, job_prefix=job_prefix)
