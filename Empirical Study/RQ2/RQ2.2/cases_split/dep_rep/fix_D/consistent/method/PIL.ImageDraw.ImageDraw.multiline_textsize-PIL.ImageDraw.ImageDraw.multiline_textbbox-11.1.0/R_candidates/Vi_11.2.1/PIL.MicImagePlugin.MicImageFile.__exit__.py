    def __exit__(self, *args: object) -> None:
        self.__fp.close()
        self.ole.close()
        super().__exit__()
