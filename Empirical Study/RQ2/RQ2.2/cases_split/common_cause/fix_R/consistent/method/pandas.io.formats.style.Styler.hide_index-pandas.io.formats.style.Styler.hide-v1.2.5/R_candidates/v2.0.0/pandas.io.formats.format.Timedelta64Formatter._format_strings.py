    def _format_strings(self) -> list[str]:
        formatter = self.formatter or get_format_timedelta64(
            self.values, nat_rep=self.nat_rep, box=self.box
        )
        return [formatter(x) for x in self.values]
