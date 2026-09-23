def _get_job_times_json(job_times: Dict[str, float]) -> JobTimeJSON:
    return {
        'commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], encoding="ascii").strip(),
        'JOB_BASE_NAME': _get_stripped_CI_job(),
        'job_times': job_times,
    }
