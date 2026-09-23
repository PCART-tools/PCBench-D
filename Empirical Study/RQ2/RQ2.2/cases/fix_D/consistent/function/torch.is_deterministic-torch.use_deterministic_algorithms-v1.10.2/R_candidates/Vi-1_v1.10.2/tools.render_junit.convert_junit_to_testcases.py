def convert_junit_to_testcases(xml: Union[JUnitXml, TestSuite]) -> List[TestCase]:  # type: ignore[no-any-unimported]
    testcases = []
    for item in xml:
        if isinstance(item, TestSuite):
            testcases.extend(convert_junit_to_testcases(item))
        else:
            testcases.append(item)
    return testcases
