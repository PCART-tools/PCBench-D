def get_font(filename, hinting_factor=None):
    # Resolving the path avoids embedding the font twice in pdf/ps output if a
    # single font is selected using two different relative paths.
    filename = _cached_realpath(filename)
    if hinting_factor is None:
        hinting_factor = rcParams['text.hinting_factor']
    # also key on the thread ID to prevent segfaults with multi-threading
    return _get_font(filename, hinting_factor,
                     _kerning_factor=rcParams['text.kerning_factor'],
                     thread_id=threading.get_ident())
