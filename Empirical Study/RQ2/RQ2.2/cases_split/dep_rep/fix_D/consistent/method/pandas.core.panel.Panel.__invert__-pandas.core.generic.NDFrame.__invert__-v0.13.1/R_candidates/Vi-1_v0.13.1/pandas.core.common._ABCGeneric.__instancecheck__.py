    def __instancecheck__(cls, inst):
        return hasattr(inst, "_data")
