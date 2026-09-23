class ThreadSafeStore(object):
    def __init__(self):
        self.concurrent_uses = 0
        self.max_concurrent_uses = 0

    def __setitem__(self, key, value):
        self.concurrent_uses += 1
        self.max_concurrent_uses = max(self.concurrent_uses, self.max_concurrent_uses)
        time.sleep(0.01)
        self.concurrent_uses -= 1
