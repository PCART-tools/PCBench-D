def argument_type_size(t: Type) -> Optional[int]:
    l = t.is_list_like()
    if l is not None and str(l.elem) != 'bool':
        return l.size
    else:
        return None
