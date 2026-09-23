    def _construct_result(self, result, name):
        if isinstance(result, tuple):
            return (
                Index._with_infer(result[0], name=name),
                Index._with_infer(result[1], name=name),
            )
        return Index._with_infer(result, name=name)
