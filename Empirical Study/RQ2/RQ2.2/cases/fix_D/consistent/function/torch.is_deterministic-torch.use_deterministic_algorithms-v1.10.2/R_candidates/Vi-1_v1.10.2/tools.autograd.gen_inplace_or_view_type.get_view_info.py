def get_view_info(fn: NativeFunctionWithDifferentiabilityInfo) -> Optional[str]:
    f = fn.func
    base_name = get_base_name(f)
    view_info = VIEW_FUNCTIONS.get(base_name, None)
    if view_info is None and base_name in RETURNS_VIEWS_OF_INPUT:
        view_info = "self"
    return view_info
