def _write_local_header(fp, im, offset, flags):
    transparent_color_exists = False
    try:
        transparency = im.encoderinfo["transparency"]
    except KeyError:
        pass
    else:
        transparency = int(transparency)
        # optimize the block away if transparent color is not used
        transparent_color_exists = True

        used_palette_colors = _get_optimize(im, im.encoderinfo)
        if used_palette_colors is not None:
            # adjust the transparency index after optimize
            try:
                transparency = used_palette_colors.index(transparency)
            except ValueError:
                transparent_color_exists = False

    if "duration" in im.encoderinfo:
        duration = int(im.encoderinfo["duration"] / 10)
    else:
        duration = 0

    disposal = int(im.encoderinfo.get("disposal", 0))

    if transparent_color_exists or duration != 0 or disposal:
        packed_flag = 1 if transparent_color_exists else 0
        packed_flag |= disposal << 2
        if not transparent_color_exists:
            transparency = 0

        fp.write(
            b"!"
            + o8(249)  # extension intro
            + o8(4)  # length
            + o8(packed_flag)  # packed fields
            + o16(duration)  # duration
            + o8(transparency)  # transparency index
            + o8(0)
        )

    if "comment" in im.encoderinfo and 1 <= len(im.encoderinfo["comment"]):
        fp.write(b"!" + o8(254))  # extension intro
        comment = im.encoderinfo["comment"]
        if isinstance(comment, str):
            comment = comment.encode()
        for i in range(0, len(comment), 255):
            subblock = comment[i : i + 255]
            fp.write(o8(len(subblock)) + subblock)
        fp.write(o8(0))
    if "loop" in im.encoderinfo:
        number_of_loops = im.encoderinfo["loop"]
        fp.write(
            b"!"
            + o8(255)  # extension intro
            + o8(11)
            + b"NETSCAPE2.0"
            + o8(3)
            + o8(1)
            + o16(number_of_loops)  # number of loops
            + o8(0)
        )
    include_color_table = im.encoderinfo.get("include_color_table")
    if include_color_table:
        palette_bytes = _get_palette_bytes(im)
        color_table_size = _get_color_table_size(palette_bytes)
        if color_table_size:
            flags = flags | 128  # local color table flag
            flags = flags | color_table_size

    fp.write(
        b","
        + o16(offset[0])  # offset
        + o16(offset[1])
        + o16(im.size[0])  # size
        + o16(im.size[1])
        + o8(flags)  # flags
    )
    if include_color_table and color_table_size:
        fp.write(_get_header_palette(palette_bytes))
    fp.write(o8(8))  # bits
