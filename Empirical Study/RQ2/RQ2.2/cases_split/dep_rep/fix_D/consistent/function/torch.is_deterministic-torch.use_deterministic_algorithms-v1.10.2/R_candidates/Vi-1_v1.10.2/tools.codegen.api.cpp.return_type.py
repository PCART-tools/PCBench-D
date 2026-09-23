def return_type(r: Return) -> CType:
    return returntype_type(r.type, mutable=r.is_write)
