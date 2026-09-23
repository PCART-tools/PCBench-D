    def is_rref(ann) -> bool:
        if ann is RRef:
            raise RuntimeError(
                "Attempted to use RRef without a "
                "contained type. Please add a contained type, e.g. "
                "RRef[int]"
            )
        return get_origin(ann) is RRef
