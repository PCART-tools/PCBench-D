def is_this_type_of_tests(target_name: str, test_set_by_type: Set[str]) -> bool:
    # tests are divided into three types: success / partial success / fail to collect coverage
    for test in test_set_by_type:
        if target_name in test:
            return True
    return False
