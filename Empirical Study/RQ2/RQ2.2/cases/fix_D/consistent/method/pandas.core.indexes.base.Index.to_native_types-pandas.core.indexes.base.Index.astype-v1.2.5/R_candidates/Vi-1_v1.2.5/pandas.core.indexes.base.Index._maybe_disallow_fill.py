    def _maybe_disallow_fill(self, allow_fill: bool, fill_value, indices) -> bool:
        """
        We only use pandas-style take when allow_fill is True _and_
        fill_value is not None.
        """
        if allow_fill and fill_value is not None:
            # only fill if we are passing a non-None fill_value
            if self._can_hold_na:
                if (indices < -1).any():
                    raise ValueError(
                        "When allow_fill=True and fill_value is not None, "
                        "all indices must be >= -1"
                    )
            else:
                cls_name = type(self).__name__
                raise ValueError(
                    f"Unable to fill values because {cls_name} cannot contain NA"
                )
        else:
            allow_fill = False
        return allow_fill
