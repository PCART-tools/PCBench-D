def gen_input(testcase):
    if "input_size" in testcase:
        if testcase["input_size"] == () and "desc" in testcase and testcase["desc"][-6:] == "scalar":
            testcase["input_size"] = (1,)
        return Variable(torch.randn(*testcase["input_size"]))
    elif "input_fn" in testcase:
        input = testcase["input_fn"]()
        if isinstance(input, Variable):
            return input
        return Variable(testcase["input_fn"]())
