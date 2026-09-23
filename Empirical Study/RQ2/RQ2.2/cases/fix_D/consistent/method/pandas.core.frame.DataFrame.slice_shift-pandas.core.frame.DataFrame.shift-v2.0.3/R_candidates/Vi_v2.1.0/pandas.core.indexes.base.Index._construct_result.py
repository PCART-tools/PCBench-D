    @final
    def _construct_result(self, result, name):
        if isinstance(result, tuple):
            return (
                Index(result[0], name=name, dtype=result[0].dtype),
                Index(result[1], name=name, dtype=result[1].dtype),
            )
        return Index(result, name=name, dtype=result.dtype)
