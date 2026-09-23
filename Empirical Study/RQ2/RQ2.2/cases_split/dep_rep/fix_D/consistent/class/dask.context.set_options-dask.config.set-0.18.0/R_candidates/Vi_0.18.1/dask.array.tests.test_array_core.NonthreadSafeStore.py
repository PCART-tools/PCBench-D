class NonthreadSafeStore(object):
    def __init__(self):
        self.in_use = False

    def __setitem__(self, key, value):
        if self.in_use:
            raise ThreadSafetyError()
        self.in_use = True
        time.sleep(0.001)
        self.in_use = False
