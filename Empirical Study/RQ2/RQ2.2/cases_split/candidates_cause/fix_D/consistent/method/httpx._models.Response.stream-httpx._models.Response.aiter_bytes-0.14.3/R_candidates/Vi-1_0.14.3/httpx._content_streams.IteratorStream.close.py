    def close(self) -> None:
        if self.close_func is not None:
            self.close_func()
