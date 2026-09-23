def canonical_name(opname: str) -> str:
    # Skip the overload name part as it's not supported by code analyzer yet.
    return opname.split('.', 1)[0]
