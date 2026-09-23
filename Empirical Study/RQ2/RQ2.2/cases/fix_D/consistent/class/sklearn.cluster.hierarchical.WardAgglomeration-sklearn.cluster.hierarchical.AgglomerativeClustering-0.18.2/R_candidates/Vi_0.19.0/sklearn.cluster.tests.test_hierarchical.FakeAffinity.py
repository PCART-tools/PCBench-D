    class FakeAffinity:
        def __init__(self):
            self.counter = 0

        def increment(self, *args, **kwargs):
            self.counter += 1
            return self.counter
