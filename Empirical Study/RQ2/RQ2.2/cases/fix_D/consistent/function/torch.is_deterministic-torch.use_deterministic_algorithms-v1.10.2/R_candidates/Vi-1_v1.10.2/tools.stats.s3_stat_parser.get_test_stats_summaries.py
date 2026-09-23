def get_test_stats_summaries(*, sha: str, jobs: Optional[List[str]] = None) -> Dict[str, List[Report]]:
    bucket = get_S3_bucket_readonly(OSSCI_METRICS_BUCKET)
    summaries = bucket.objects.filter(Prefix=f"test_time/{sha}")
    return _parse_master_summaries(summaries, jobs=list(jobs or []))
