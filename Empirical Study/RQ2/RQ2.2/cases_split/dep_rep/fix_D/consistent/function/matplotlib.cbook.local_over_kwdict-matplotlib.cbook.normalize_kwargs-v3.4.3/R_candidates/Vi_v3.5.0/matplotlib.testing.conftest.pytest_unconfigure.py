def pytest_unconfigure(config):
    matplotlib._called_from_pytest = False
