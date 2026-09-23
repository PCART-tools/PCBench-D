def _detach_and_copy_item_memo(t):
    detached_t = t.detach()
    if hasattr(t, "item_memo"):
        detached_t.item_memo = t.item_memo
    return detached_t
