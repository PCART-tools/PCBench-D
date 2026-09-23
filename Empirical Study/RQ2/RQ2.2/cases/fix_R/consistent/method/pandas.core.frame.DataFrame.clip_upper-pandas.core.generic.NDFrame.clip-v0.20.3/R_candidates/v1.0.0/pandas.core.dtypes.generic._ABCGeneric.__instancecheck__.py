    def __instancecheck__(cls, inst) -> bool:
        return hasattr(inst, "_data")
