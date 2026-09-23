    def __init__(self, fn, new=False):
        if hasattr(fn, "read"):
            self.f = fn
            self.close_fp = False
        else:
            self.name = fn
            self.close_fp = True
            try:
                self.f = open(fn, "w+b" if new else "r+b")
            except OSError:
                self.f = open(fn, "w+b")
        self.beginning = self.f.tell()
        self.setup()
