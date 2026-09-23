    def _sk_visual_block_(self):
        if isinstance(self.remainder, str) and self.remainder == "drop":
            transformers = self.transformers
        elif hasattr(self, "_remainder"):
            remainder_columns = self._remainder[2]
            if (
                hasattr(self, "feature_names_in_")
                and remainder_columns
                and not all(isinstance(col, str) for col in remainder_columns)
            ):
                remainder_columns = self.feature_names_in_[remainder_columns].tolist()
            transformers = chain(
                self.transformers, [("remainder", self.remainder, remainder_columns)]
            )
        else:
            transformers = chain(self.transformers, [("remainder", self.remainder, "")])

        names, transformers, name_details = zip(*transformers)
        return _VisualBlock(
            "parallel", transformers, names=names, name_details=name_details
        )
