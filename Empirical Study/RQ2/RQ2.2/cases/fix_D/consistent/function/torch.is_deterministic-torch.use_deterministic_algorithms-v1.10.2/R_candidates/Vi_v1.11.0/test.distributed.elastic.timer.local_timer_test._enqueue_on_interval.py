    def _enqueue_on_interval(mp_queue, n, interval, sem):
        """
        enqueues ``n`` timer requests into ``mp_queue`` one element per
        interval seconds. Releases the given semaphore once before going to work.
        """
        sem.release()
        for i in range(0, n):
            mp_queue.put(TimerRequest(i, "test_scope", 0))
            time.sleep(interval)
