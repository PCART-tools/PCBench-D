    def _parse_with_reso(self, label: str):
        # the "with_reso" is a no-op for TimedeltaIndex
        parsed = Timedelta(label)
        return parsed, None
