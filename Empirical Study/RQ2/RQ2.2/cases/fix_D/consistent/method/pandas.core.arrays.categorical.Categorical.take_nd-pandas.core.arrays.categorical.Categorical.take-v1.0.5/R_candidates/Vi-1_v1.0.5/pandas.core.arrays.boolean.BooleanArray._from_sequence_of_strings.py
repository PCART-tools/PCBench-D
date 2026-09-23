    @classmethod
    def _from_sequence_of_strings(
        cls, strings: List[str], dtype=None, copy: bool = False
    ):
        def map_string(s):
            if isna(s):
                return s
            elif s in ["True", "TRUE", "true"]:
                return True
            elif s in ["False", "FALSE", "false"]:
                return False
            else:
                raise ValueError(f"{s} cannot be cast to bool")

        scalars = [map_string(x) for x in strings]
        return cls._from_sequence(scalars, dtype, copy)
