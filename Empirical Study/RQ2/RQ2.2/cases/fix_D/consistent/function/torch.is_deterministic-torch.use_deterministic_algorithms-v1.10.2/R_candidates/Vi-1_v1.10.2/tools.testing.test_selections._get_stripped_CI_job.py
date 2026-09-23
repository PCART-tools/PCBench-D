def _get_stripped_CI_job() -> str:
    """E.g. convert 'pytorch_windows_vs2019_py36_cuda10.1_build' to 'pytorch_windows_vs2019_py36_cuda10.1'.
    """
    job = os.environ.get("JOB_BASE_NAME", "").rstrip('0123456789')
    if job.endswith('_slow_test'):
        job = job[:len(job) - len('_slow_test')]
    elif job.endswith('_test') or job.endswith('-test'):
        job = job[:len(job) - len('_test')]
    elif job.endswith('_build') or job.endswith('-build'):
        job = job[:len(job) - len('_build')]
    return job
