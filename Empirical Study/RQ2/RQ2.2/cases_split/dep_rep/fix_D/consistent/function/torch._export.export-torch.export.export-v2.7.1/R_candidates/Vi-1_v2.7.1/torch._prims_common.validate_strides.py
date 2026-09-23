def validate_strides(strides: StrideType):
    """
    Verifies the object specifies valid strides.
    """

    assert isinstance(strides, Sequence)
    for stride in strides:
        assert stride >= 0
