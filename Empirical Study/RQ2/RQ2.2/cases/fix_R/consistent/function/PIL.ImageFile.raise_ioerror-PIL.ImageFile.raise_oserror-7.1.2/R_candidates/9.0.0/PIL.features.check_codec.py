def check_codec(feature):
    """
    Checks if a codec is available.

    :param feature: The codec to check for.
    :returns: ``True`` if available, ``False`` otherwise.
    :raises ValueError: If the codec is not defined in this version of Pillow.
    """
    if feature not in codecs:
        raise ValueError(f"Unknown codec {feature}")

    codec, lib = codecs[feature]

    return codec + "_encoder" in dir(Image.core)
