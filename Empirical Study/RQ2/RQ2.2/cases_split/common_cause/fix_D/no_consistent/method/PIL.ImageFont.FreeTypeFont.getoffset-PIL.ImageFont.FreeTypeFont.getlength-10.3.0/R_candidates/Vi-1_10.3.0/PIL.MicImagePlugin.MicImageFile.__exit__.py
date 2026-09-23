    def __exit__(self, *args):
        self.__fp.close()
        self.ole.close()
        super().__exit__()
