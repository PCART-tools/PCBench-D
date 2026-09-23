def pytest_ignore_collect(path, config):
    "Skip this directory if distributed modules are not enabled."
    return not dist.is_available()
