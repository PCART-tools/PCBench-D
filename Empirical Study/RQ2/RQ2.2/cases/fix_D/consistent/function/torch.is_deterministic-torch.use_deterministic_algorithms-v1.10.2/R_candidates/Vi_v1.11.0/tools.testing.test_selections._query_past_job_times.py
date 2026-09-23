def _query_past_job_times(test_times_file: Optional[str] = None) -> Dict[str, float]:
    """Read historic test job times from a file.

    If the file doesn't exist or isn't matching current commit. It will download data from S3 and exported it.
    """
    if test_times_file and os.path.exists(test_times_file):
        with open(test_times_file) as file:
            test_times_json: JobTimeJSON = json.load(file)

        curr_commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], encoding="ascii").strip()
        file_commit = test_times_json.get('commit', '')
        curr_ci_job = _get_stripped_CI_job()
        file_ci_job = test_times_json.get('JOB_BASE_NAME', 'N/A')
        if curr_commit != file_commit:
            print(f'Current test times file is from different commit {file_commit}.')
        elif curr_ci_job != file_ci_job:
            print(f'Current test times file is for different CI job {file_ci_job}.')
        else:
            print(f'Found stats for current commit: {curr_commit} and job: {curr_ci_job}. Proceeding with those values.')
            return test_times_json.get('job_times', {})

        # Found file, but commit or CI job in JSON doesn't match
        print(f'Overwriting current file with stats based on current commit: {curr_commit} and CI job: {curr_ci_job}')

    job_times = export_S3_test_times(test_times_file)

    return job_times
