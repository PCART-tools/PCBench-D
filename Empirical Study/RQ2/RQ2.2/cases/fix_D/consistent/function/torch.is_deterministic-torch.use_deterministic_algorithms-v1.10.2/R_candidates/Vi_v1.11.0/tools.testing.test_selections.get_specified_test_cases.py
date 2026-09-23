def get_specified_test_cases(filename: str, tests: List[str]) -> Dict[str, List[str]]:
    """Get test cases from a specified test case file. Usually exported manually or through CI system.
    """
    if not os.path.exists(filename):
        print(f'Could not find specified tests file: {filename}. Proceeding with default behavior.')
        return dict()

    # The below encoding is utf-8-sig because utf-8 doesn't properly handle the byte-order-mark character
    with open(filename, mode='r', encoding="utf-8-sig") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        specified_test_case_dict: Dict[str, List[str]] = dict()
        for row in csv_reader:
            line_count += 1
            if line_count == 1:
                if 'test_filename' not in row or 'test_case_name' not in row:
                    print('Data is missing necessary columns for test specification. Proceeding with default behavior.')
                    return dict()
            test_filename = row['test_filename']
            test_case_name = row['test_case_name']
            if test_filename not in tests:
                print(f'Specified test_filename {test_filename} not found in TESTS. Skipping.')
                continue
            if test_filename not in specified_test_case_dict:
                specified_test_case_dict[test_filename] = []
            specified_test_case_dict[test_filename].append(test_case_name)
        print(f'Processed {line_count} test cases.')
        return specified_test_case_dict
