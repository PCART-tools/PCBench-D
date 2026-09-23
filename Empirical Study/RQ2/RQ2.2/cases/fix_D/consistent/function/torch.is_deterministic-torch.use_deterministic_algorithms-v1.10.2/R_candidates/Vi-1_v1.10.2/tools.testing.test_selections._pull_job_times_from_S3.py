def _pull_job_times_from_S3() -> Dict[str, float]:
    if HAVE_BOTO3:
        ci_job_prefix = _get_stripped_CI_job()
        s3_reports: List["Report"] = get_previous_reports_for_branch('origin/viable/strict', ci_job_prefix)
    else:
        print('Uh oh, boto3 is not found. Either it is not installed or we failed to import s3_stat_parser.')
        print('If not installed, please install boto3 for automatic sharding and test categorization.')
        s3_reports = []

    if len(s3_reports) == 0:
        print('Gathered no reports from S3. Please proceed without them.')
        return dict()

    return _calculate_job_times(s3_reports)
