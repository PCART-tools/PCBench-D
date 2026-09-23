@_format_argument.register
def _tuple(obj: tuple) -> str:
    tuple_string = f"Tuple[length={len(obj)}](\n"
    if not obj:
        return tuple_string + "None)"
    for i, item in enumerate(obj):
        if i >= _CONTAINER_ITEM_LIMIT:
            # NOTE: Print only first _CONTAINER_ITEM_LIMIT items.
            tuple_string += "...,\n"
            break
        tuple_string += f"{format_argument(item)},\n"
    return tuple_string + ")"
