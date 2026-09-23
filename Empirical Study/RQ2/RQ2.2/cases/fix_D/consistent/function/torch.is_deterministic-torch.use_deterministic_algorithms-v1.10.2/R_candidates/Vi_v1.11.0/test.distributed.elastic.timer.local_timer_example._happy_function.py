def _happy_function(rank, mp_queue):
    timer.configure(timer.LocalTimerClient(mp_queue))
    with timer.expires(after=1):
        time.sleep(0.5)
