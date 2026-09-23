    def _get_level_number(self, level) -> int:
        count = self.names.count(level)
        if (count > 1) and not is_integer(level):
            raise ValueError(
                f"The name {level} occurs multiple times, use a level number"
            )
        try:
            level = self.names.index(level)
        except ValueError as err:
            if not is_integer(level):
                raise KeyError(f"Level {level} not found") from err
            if level < 0:
                level += self.nlevels
                if level < 0:
                    orig_level = level - self.nlevels
                    raise IndexError(
                        f"Too many levels: Index has only {self.nlevels} levels, "
                        f"{orig_level} is not a valid level number"
                    ) from err
            # Note: levels are zero-based
            elif level >= self.nlevels:
                raise IndexError(
                    f"Too many levels: Index has only {self.nlevels} levels, "
                    f"not {level + 1}"
                ) from err
        return level
