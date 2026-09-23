def get_test_name(testcase):
    if "fullname" in testcase:
        return "test_" + testcase["fullname"]

    test_name = "test_" + testcase["constructor"].__name__
    if "desc" in testcase:
        test_name += "_" + testcase["desc"]
    return test_name
