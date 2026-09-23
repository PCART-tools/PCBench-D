def _save(im, fp, filename):
    if filename.endswith(".j2k"):
        kind = "j2k"
    else:
        kind = "jp2"

    # Get the keyword arguments
    info = im.encoderinfo

    offset = info.get("offset", None)
    tile_offset = info.get("tile_offset", None)
    tile_size = info.get("tile_size", None)
    quality_mode = info.get("quality_mode", "rates")
    quality_layers = info.get("quality_layers", None)
    if quality_layers is not None and not (
        isinstance(quality_layers, (list, tuple))
        and all(
            [
                isinstance(quality_layer, (int, float))
                for quality_layer in quality_layers
            ]
        )
    ):
        raise ValueError("quality_layers must be a sequence of numbers")

    num_resolutions = info.get("num_resolutions", 0)
    cblk_size = info.get("codeblock_size", None)
    precinct_size = info.get("precinct_size", None)
    irreversible = info.get("irreversible", False)
    progression = info.get("progression", "LRCP")
    cinema_mode = info.get("cinema_mode", "no")
    fd = -1

    if hasattr(fp, "fileno"):
        try:
            fd = fp.fileno()
        except Exception:
            fd = -1

    im.encoderconfig = (
        offset,
        tile_offset,
        tile_size,
        quality_mode,
        quality_layers,
        num_resolutions,
        cblk_size,
        precinct_size,
        irreversible,
        progression,
        cinema_mode,
        fd,
    )

    ImageFile._save(im, fp, [("jpeg2k", (0, 0) + im.size, 0, kind)])
