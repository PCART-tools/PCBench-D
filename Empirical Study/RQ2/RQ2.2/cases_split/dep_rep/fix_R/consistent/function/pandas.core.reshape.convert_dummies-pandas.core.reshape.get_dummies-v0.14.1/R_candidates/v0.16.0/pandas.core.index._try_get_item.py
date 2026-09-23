def _try_get_item(x):
    try:
        return x.item()
    except AttributeError:
        return x
