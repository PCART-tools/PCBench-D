    def close(self) -> None:
        self.__fp.close()
        self.ole.close()
        super().close()
