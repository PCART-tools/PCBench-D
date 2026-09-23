    def __exit__(self, *args):
        self.ole.close()
        super().__exit__()
