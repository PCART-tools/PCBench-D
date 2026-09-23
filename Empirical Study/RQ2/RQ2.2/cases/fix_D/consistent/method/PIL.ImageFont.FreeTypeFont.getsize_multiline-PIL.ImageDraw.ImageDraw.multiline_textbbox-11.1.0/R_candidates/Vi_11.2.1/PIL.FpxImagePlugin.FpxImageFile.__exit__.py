    def __exit__(self, *args: object) -> None:
        self.ole.close()
        super().__exit__()
