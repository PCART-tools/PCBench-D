    def __init__(self, path):
        self.path = path
        self.end = "-" + str(os.getpid())
        self.lock_path = os.path.join(self.path, self.LOCKFN + self.end)
        self.pattern = os.path.join(self.path, self.LOCKFN + '-*')
        self.remove = True
