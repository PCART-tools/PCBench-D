def update_equivalent_types_dict(customized_equivalent_types=None):
    """Help function for user who wants to customize the _EQUIVALENT_TYPES and _EQUIVALENT_TYPES_DICT.
    When customized_equivalent_types passes in,
    re-generate _EQUIVALENT_TYPES and _EQUIVALENT_TYPES_DICT.
    """
    if customized_equivalent_types is None:
        raise ValueError("customized_equivalent_types should not be None")
    global _EQUIVALENT_TYPES
    global _EQUIVALENT_TYPES_DICT
    _EQUIVALENT_TYPES = customized_equivalent_types
    _EQUIVALENT_TYPES_DICT = _create_equivalent_types_dict()
