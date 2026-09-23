def get_test_stats_summaries_for_job(*, sha: str, job_prefix: str) -> Dict[str, List[Report]]:
    bucket = get_S3_bucket_readonly(OSSCI_METRICS_BUCKET)
    summaries = bucket.objects.filter(Prefix=f"test_time/{sha}/{job_prefix}")
    return _parse_master_summaries(summaries, jobs=list())
