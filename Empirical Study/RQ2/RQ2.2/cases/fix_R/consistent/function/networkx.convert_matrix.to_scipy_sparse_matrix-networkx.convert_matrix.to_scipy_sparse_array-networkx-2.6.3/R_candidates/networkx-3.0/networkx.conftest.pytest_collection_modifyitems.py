def pytest_collection_modifyitems(config, items):
    # Allow pluggable backends to add markers to tests when
    # running in auto-conversion test mode
    networkx.classes.backends._mark_tests(items)

    if config.getoption("--runslow"):
        # --runslow given in cli: do not skip slow tests
        return
    skip_slow = pytest.mark.skip(reason="need --runslow option to run")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)
