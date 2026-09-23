def __getattr__(name):
    categories = {"NORMAL": 0, "SEQUENCE": 1, "CONTAINER": 2}
    if name in categories:
        warnings.warn(
            "Image categories are deprecated and will be removed in Pillow 10 "
            "(2023-07-01). Use is_animated instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return categories[name]
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
