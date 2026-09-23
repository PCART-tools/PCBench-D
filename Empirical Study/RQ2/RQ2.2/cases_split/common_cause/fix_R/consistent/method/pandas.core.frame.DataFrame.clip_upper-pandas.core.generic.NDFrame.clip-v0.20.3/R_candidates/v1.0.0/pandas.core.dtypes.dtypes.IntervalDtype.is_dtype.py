    @classmethod
    def is_dtype(cls, dtype) -> bool:
        """
        Return a boolean if we if the passed type is an actual dtype that we
        can match (via string or type)
        """

        if isinstance(dtype, str):
            if dtype.lower().startswith("interval"):
                try:
                    if cls.construct_from_string(dtype) is not None:
                        return True
                    else:
                        return False
                except (ValueError, TypeError):
                    return False
            else:
                return False
        return super().is_dtype(dtype)
