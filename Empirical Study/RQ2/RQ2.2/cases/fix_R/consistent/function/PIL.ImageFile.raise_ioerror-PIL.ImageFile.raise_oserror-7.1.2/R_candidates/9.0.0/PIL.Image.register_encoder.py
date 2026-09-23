def register_encoder(name, encoder):
    """
    Registers an image encoder.  This function should not be
    used in application code.

    :param name: The name of the encoder
    :param encoder: A callable(mode, args) that returns an
                    ImageFile.PyEncoder object

    .. versionadded:: 4.1.0
    """
    ENCODERS[name] = encoder
