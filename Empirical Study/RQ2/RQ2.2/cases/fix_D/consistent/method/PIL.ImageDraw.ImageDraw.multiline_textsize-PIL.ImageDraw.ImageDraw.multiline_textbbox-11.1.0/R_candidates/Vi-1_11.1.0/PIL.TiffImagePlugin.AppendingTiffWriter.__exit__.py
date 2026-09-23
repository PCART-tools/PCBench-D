    def __exit__(self, *args: object) -> None:
        if self.close_fp:
            self.close()
