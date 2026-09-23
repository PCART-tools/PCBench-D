def too_similar(calculated_times: Dict[str, float], other_times: Dict[str, float], threshold: float) -> bool:
    # check that their keys are the same
    if calculated_times.keys() != other_times.keys():
        return False

    for test_case, test_time in calculated_times.items():
        other_test_time = other_times[test_case]
        relative_difference = abs((other_test_time - test_time) / max(other_test_time, test_time))
        if relative_difference > threshold:
            return False
    return True
