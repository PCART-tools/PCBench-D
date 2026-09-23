def _to_string(x: Union[int, float, str, List]) -> str:
    if isinstance(x, list):
        val_list = ",".join(str(val) for val in x)
        return f"[{val_list}]"
    else:
        return str(x)
