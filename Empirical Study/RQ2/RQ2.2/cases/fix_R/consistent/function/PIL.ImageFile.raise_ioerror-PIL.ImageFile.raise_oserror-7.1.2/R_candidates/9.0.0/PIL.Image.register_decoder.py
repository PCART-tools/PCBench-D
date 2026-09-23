def register_decoder(name, decoder):
    """
    Registers an image decoder.  This function should not be
    used in application code.

    :param name: The name of the decoder
    :param decoder: A callable(mode, args) that returns an
                    ImageFile.PyDecoder object

    .. versionadded:: 4.1.0
    """
    DECODERS[name] = decoder
