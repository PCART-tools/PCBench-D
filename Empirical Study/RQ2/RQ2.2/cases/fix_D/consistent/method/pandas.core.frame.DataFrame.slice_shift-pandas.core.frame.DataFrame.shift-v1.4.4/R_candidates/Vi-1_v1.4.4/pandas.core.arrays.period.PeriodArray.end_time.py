    @property
    def end_time(self) -> DatetimeArray:
        return self.to_timestamp(how="end")
