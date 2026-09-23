def pytest_addoption(parser):
    parser.addoption("--fuser", default="old", help="fuser to use for benchmarks")
    parser.addoption("--executor", default="legacy", help="executor to use for benchmarks")
