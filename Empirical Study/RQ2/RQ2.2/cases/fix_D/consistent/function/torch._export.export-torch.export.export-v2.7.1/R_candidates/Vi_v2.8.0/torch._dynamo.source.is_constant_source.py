def is_constant_source(source):
    if isinstance(source, ConstantSource):
        return True
    try:
        if source.guard_source() == GuardSource.CONSTANT:
            return True
    except NotImplementedError:
        pass

    return False
