@pytest.fixture(autouse=True)
def skip_tracker():
    skip_tracker = SkipTracker()
    with use_skip_tracker(skip_tracker):
        yield skip_tracker
