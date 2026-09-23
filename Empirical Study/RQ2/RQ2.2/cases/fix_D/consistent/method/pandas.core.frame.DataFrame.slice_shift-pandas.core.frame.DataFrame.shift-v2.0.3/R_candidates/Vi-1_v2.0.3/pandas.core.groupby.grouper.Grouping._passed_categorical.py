    @cache_readonly
    def _passed_categorical(self) -> bool:
        return is_categorical_dtype(self.grouping_vector)
