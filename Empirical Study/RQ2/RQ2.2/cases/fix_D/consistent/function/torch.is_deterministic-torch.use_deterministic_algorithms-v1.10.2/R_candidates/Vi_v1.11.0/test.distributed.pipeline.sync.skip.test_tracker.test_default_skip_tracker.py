def test_default_skip_tracker():
    q = Queue()

    def f():
        q.put(current_skip_tracker())

    t = threading.Thread(target=f)
    t.start()
    t.join()

    skip_tracker = q.get()

    assert type(skip_tracker) is SkipTracker
    assert type(skip_tracker) is not SkipTrackerThroughPotals
