    def end_group(self) -> T.Any:
        self.pop_state()
        return []
