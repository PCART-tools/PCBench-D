def reinforce_type(self, expected_type):
    r"""
    Reinforce the type for DataPipe instance. And the 'expected_type' is required
    to be a subtype of the original type hint to restrict the type requirement
    of DataPipe instance.
    """
    if isinstance(expected_type, tuple):
        expected_type = Tuple[expected_type]
    _type_check(expected_type, msg="'expected_type' must be a type")

    if not issubtype(expected_type, self.type.param):
        raise TypeError("Expected 'expected_type' as subtype of {}, but found {}"
                        .format(self.type, _type_repr(expected_type)))

    self.type = _DataPipeType(expected_type)
    return self
