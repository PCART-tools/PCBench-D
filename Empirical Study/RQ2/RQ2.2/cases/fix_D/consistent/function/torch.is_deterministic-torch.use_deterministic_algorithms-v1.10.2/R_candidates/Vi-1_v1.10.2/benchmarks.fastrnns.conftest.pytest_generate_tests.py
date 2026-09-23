def pytest_generate_tests(metafunc):
    # This creates lists of tests to generate, can be customized
    if metafunc.cls.__name__ == "TestBenchNetwork":
        metafunc.parametrize('net_name', all_nets, scope="class")
        metafunc.parametrize("executor", [metafunc.config.getoption("executor")], scope="class")
        metafunc.parametrize("fuser", [metafunc.config.getoption("fuser")], scope="class")
