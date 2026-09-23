    def take_nd(self, indexer, allow_fill: bool = False, fill_value=None):
        # GH#27745 deprecate alias that other EAs dont have
        warn(
            "Categorical.take_nd is deprecated, use Categorical.take instead",
            FutureWarning,
            stacklevel=find_stack_level(),
        )
        return self.take(indexer, allow_fill=allow_fill, fill_value=fill_value)
