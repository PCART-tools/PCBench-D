def parse_report(path: str) -> Iterator[TestCase]:
    try:
        dom = minidom.parse(path)
    except Exception as e:
        print(f"Error occurred when parsing {path}: {e}")
        return
    for test_case in dom.getElementsByTagName('testcase'):
        yield TestCase(test_case)
