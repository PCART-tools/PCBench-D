@_format_argument.register
def _list(obj: list) -> str:
    list_string = f"List[length={len(obj)}](\n"
    if not obj:
        return list_string + "None)"
    for i, item in enumerate(obj):
        if i >= _CONTAINER_ITEM_LIMIT:
            # NOTE: Print only first _CONTAINER_ITEM_LIMIT items.
            list_string += "...,\n"
            break
        list_string += f"{format_argument(item)},\n"
    return list_string + ")"
