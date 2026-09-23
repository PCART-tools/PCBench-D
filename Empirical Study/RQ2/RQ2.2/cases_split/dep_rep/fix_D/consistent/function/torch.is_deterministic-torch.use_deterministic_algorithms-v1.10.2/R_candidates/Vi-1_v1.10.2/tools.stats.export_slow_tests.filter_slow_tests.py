def filter_slow_tests(test_cases_dict: Dict[str, float]) -> Dict[str, float]:
    return {test_case: time for test_case, time in test_cases_dict.items() if time >= SLOW_TEST_CASE_THRESHOLD_SEC}
