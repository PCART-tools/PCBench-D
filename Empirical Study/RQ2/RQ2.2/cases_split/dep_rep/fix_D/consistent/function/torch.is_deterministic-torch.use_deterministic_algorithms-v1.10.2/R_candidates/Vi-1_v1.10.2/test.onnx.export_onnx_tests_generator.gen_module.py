def gen_module(testcase):
    if "constructor_args" in testcase:
        args = testcase["constructor_args"]
        module = testcase["constructor"](*args)
        module.train(False)
        return module
    module = testcase["constructor"]()
    module.train(False)
    return module
