    def close(self) -> None:
        self.ole.close()
        super().close()
