def _getdecoder(mode, decoder_name, args, extra=()):

    # tweak arguments
    if args is None:
        args = ()
    elif not isinstance(args, tuple):
        args = (args,)

    try:
        decoder = DECODERS[decoder_name]
    except KeyError:
        pass
    else:
        return decoder(mode, *args + extra)

    try:
        # get decoder
        decoder = getattr(core, decoder_name + "_decoder")
    except AttributeError as e:
        raise OSError(f"decoder {decoder_name} not available") from e
    return decoder(mode, *args + extra)
