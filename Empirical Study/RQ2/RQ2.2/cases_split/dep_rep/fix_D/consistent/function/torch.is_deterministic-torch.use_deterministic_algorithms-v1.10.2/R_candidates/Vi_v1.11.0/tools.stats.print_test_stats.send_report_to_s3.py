def send_report_to_s3(head_report: Version2Report) -> None:
    job = os.getenv('JOB_BASE_NAME', os.environ.get('CIRCLE_JOB'))
    sha1 = os.environ.get('SHA1', os.environ.get('CIRCLE_SHA1', ''))
    branch = os.environ.get('BRANCH', os.environ.get('CIRCLE_BRANCH', ''))
    now = datetime.datetime.utcnow().isoformat()

    # SHARD_NUMBER and TEST_CONFIG are specific to GHA, as these details would be included in CIRCLE_JOB already
    shard = os.environ.get('SHARD_NUMBER', '')
    test_config = os.environ.get('TEST_CONFIG')

    job_report_dirname = f'{job}{f"-{test_config}" if test_config is not None else ""}{shard}'

    if branch not in ['master', 'nightly'] and not branch.startswith("release/"):
        pr = os.environ.get('PR_NUMBER', os.environ.get('CIRCLE_PR_NUMBER', 'unknown'))
        key = f'pr_test_time/{pr}/{sha1}/{job_report_dirname}/{now}Z.json.bz2'  # Z meaning UTC
    else:
        key = f'test_time/{sha1}/{job_report_dirname}/{now}Z.json.bz2'  # Z meaning UTC
    obj = get_S3_object_from_bucket('ossci-metrics', key)
    # use bz2 because the results are smaller than gzip, and the
    # compression time penalty we pay is only about half a second for
    # input files of a few megabytes in size like these JSON files, and
    # because for some reason zlib doesn't seem to play nice with the
    # gunzip command whereas Python's bz2 does work with bzip2
    obj.put(Body=bz2.compress(json.dumps(head_report).encode()))
