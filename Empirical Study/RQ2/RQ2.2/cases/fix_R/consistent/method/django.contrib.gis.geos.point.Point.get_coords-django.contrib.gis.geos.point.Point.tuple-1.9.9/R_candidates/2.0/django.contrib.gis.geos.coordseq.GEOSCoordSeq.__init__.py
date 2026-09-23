    def __init__(self, ptr, z=False):
        "Initialize from a GEOS pointer."
        if not isinstance(ptr, CS_PTR):
            raise TypeError('Coordinate sequence should initialize with a CS_PTR.')
        self._ptr = ptr
        self._z = z
