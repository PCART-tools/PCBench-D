def _for_all_items(items, functor) -> None:
    if isinstance(items, list):
        for item in items:
            _for_all_items(item, functor)
    if isinstance(items, dict) and len(items) == 1:
        item_type, item = next(iter(items.items()))
        functor(item_type, item)
