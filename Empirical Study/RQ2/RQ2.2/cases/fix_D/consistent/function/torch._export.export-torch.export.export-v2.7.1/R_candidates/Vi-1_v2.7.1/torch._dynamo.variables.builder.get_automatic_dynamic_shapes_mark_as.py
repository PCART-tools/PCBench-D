def get_automatic_dynamic_shapes_mark_as():
    if config.automatic_dynamic_shapes_mark_as == "dynamic":
        return DimDynamic.DYNAMIC
    elif config.automatic_dynamic_shapes_mark_as == "unbacked":
        return DimDynamic.SIZE_LIKE_UNBACKED
    elif config.automatic_dynamic_shapes_mark_as == "oblivious":
        return DimDynamic.OBLIVIOUS_SIZE
    else:
        raise ValueError(
            f"invalid automatic_dynamic_shapes_mark_as = {config.automatic_dynamic_shapes_mark_as}"
        )
