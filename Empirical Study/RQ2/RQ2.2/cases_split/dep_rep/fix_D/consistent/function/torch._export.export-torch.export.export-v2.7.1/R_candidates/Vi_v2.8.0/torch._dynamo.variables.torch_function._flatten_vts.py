def _flatten_vts(vts):
    from collections import deque

    from .dicts import ConstDictVariable
    from .lists import ListVariable

    vts = deque(vts)
    output = []

    while vts:
        vt = vts.pop()

        if not vt.is_realized() and vt.peek_type() in (dict, list, tuple):
            vt.realize()

        if vt.is_realized():
            if isinstance(vt, ListVariable):
                vts.extend(vt.items)
            elif isinstance(vt, ConstDictVariable):
                vts.extend(vt.items.values())

        output.append(vt)

    return output
