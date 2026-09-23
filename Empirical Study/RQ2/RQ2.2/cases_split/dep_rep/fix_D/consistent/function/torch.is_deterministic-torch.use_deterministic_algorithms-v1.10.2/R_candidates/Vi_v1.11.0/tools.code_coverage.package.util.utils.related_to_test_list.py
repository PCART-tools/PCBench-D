def related_to_test_list(file_name: str, test_list: TestList) -> bool:
    for test in test_list:
        if test.name in file_name:
            return True
    return False
