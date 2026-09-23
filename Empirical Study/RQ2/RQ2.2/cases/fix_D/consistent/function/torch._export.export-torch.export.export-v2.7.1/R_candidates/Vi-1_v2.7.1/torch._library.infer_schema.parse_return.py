def parse_return(annotation, error_fn):
    if annotation is None:
        return "()"

    if annotation is inspect.Parameter.empty:
        error_fn("No return type annotation was provided. Please add one.")

    origin = typing.get_origin(annotation)
    if origin is not tuple:
        if annotation not in SUPPORTED_RETURN_TYPES.keys():
            error_fn(
                f"Return has unsupported type {annotation}. "
                f"The valid types are: {SUPPORTED_RETURN_TYPES}."
            )
        return SUPPORTED_RETURN_TYPES[annotation]

    args = typing.get_args(annotation)
    for arg in args:
        if arg not in SUPPORTED_RETURN_TYPES:
            error_fn(
                f"Return has unsupported type {annotation}. "
                f"The valid types are: {SUPPORTED_RETURN_TYPES}."
            )

    return "(" + ", ".join([SUPPORTED_RETURN_TYPES[arg] for arg in args]) + ")"
