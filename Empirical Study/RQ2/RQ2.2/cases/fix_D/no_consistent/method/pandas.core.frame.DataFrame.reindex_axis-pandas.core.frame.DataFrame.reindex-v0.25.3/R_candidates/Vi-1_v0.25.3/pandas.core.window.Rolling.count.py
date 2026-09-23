    @Substitution(name="rolling")
    @Appender(_shared_docs["count"])
    def count(self):

        # different impl for freq counting
        if self.is_freq_type:
            return self._apply("roll_count", "count")

        return super().count()
