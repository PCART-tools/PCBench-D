def get_slow_tests_based_on_S3(test_list: List[str], td_list: List[str], slow_test_threshold: int) -> List[str]:
    """Get list of slow tests based on historic S3 data.
    """
    jobs_to_times: Dict[str, float] = _query_past_job_times()

    # Got no stats from S3, returning early to save runtime
    if len(jobs_to_times) == 0:
        print('Gathered no stats from S3. No new slow tests calculated.')
        return []

    slow_tests: List[str] = []
    for test in test_list:
        if test in jobs_to_times and test not in td_list:
            if jobs_to_times[test] > slow_test_threshold:
                slow_tests.append(test)
    return slow_tests
