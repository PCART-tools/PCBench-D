def strip_operator_overload_name(op_name: str) -> str:
    return op_name.split(".")[0]
