class CounterLock(object):
    def __init__(self, *args, **kwargs):
        self.lock = Lock(*args, **kwargs)

        self.acquire_count = 0
        self.release_count = 0

    def acquire(self, *args, **kwargs):
        self.acquire_count += 1
        return self.lock.acquire(*args, **kwargs)

    def release(self, *args, **kwargs):
        self.release_count += 1
        return self.lock.release(*args, **kwargs)
