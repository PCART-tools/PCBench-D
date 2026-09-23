def register_mime(id, mimetype):
    """
    Registers an image MIME type.  This function should not be used
    in application code.

    :param id: An image format identifier.
    :param mimetype: The image MIME type for this format.
    """
    MIME[id.upper()] = mimetype
