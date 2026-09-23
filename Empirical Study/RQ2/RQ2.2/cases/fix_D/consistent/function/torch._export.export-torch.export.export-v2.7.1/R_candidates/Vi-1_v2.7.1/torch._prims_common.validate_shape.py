def validate_shape(shape: ShapeType):
    """
    Validates that a sequence represents a valid shape.
    """

    assert isinstance(shape, Sequence), type(shape)
    for l in shape:
        validate_dim_length(l)
