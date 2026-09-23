    @classmethod
    def _from_sequence_of_strings(
        cls, strings: List[str], dtype=None, copy: bool = False
    ) -> "BooleanArray":
        def map_string(s):
            if isna(s):
                return s
            elif s in ["True", "TRUE", "true", "1", "1.0"]:
                return True
            elif s in ["False", "FALSE", "false", "0", "0.0"]:
                return False
            else:
                raise ValueError(f"{s} cannot be cast to bool")

        scalars = [map_string(x) for x in strings]
        return cls._from_sequence(scalars, dtype, copy)
