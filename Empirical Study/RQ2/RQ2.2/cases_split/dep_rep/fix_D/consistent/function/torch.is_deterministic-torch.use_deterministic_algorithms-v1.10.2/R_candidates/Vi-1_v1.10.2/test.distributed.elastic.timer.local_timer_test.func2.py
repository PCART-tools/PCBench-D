    def func2(n, mp_queue):
        if mp_queue is not None:
            timer.configure(timer.LocalTimerClient(mp_queue))
        if n > 0:
            with timer.expires(after=0.1):
                func2(n - 1, None)
                time.sleep(0.2)
