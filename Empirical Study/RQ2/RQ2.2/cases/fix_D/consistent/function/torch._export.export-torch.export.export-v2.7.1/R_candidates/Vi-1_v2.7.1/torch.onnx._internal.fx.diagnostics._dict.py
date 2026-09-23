@_format_argument.register
def _dict(obj: dict) -> str:
    dict_string = f"Dict[length={len(obj)}](\n"
    if not obj:
        return dict_string + "None)"
    for i, (key, value) in enumerate(obj.items()):
        if i >= _CONTAINER_ITEM_LIMIT:
            # NOTE: Print only first _CONTAINER_ITEM_LIMIT items.
            dict_string += "...\n"
            break
        dict_string += f"{key}: {format_argument(value)},\n"
    return dict_string + ")"
