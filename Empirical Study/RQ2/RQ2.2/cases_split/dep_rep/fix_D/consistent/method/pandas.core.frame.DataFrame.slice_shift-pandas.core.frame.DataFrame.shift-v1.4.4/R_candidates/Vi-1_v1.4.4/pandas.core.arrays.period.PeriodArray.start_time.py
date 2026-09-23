    @property
    def start_time(self) -> DatetimeArray:
        return self.to_timestamp(how="start")
