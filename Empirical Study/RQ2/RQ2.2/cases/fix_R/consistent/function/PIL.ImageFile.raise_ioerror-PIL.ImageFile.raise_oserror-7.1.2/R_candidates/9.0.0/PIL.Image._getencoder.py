def _getencoder(mode, encoder_name, args, extra=()):

    # tweak arguments
    if args is None:
        args = ()
    elif not isinstance(args, tuple):
        args = (args,)

    try:
        encoder = ENCODERS[encoder_name]
    except KeyError:
        pass
    else:
        return encoder(mode, *args + extra)

    try:
        # get encoder
        encoder = getattr(core, encoder_name + "_encoder")
    except AttributeError as e:
        raise OSError(f"encoder {encoder_name} not available") from e
    return encoder(mode, *args + extra)
