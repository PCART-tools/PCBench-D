def ann_to_type(ann, loc):
    the_type = try_ann_to_type(ann, loc)
    if the_type is not None:
        return the_type
    raise ValueError(f"Unknown type annotation: '{ann}' at {loc.highlight()}")
