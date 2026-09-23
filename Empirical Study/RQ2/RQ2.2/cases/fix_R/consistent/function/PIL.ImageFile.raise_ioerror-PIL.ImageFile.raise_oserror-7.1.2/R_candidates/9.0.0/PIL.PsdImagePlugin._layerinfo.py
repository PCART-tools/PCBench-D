def _layerinfo(fp, ct_bytes):
    # read layerinfo block
    layers = []

    def read(size):
        return ImageFile._safe_read(fp, size)

    ct = si16(read(2))

    # sanity check
    if ct_bytes < (abs(ct) * 20):
        raise SyntaxError("Layer block too short for number of layers requested")

    for i in range(abs(ct)):

        # bounding box
        y0 = i32(read(4))
        x0 = i32(read(4))
        y1 = i32(read(4))
        x1 = i32(read(4))

        # image info
        info = []
        mode = []
        ct_types = i16(read(2))
        types = list(range(ct_types))
        if len(types) > 4:
            continue

        for i in types:
            type = i16(read(2))

            if type == 65535:
                m = "A"
            else:
                m = "RGBA"[type]

            mode.append(m)
            size = i32(read(4))
            info.append((m, size))

        # figure out the image mode
        mode.sort()
        if mode == ["R"]:
            mode = "L"
        elif mode == ["B", "G", "R"]:
            mode = "RGB"
        elif mode == ["A", "B", "G", "R"]:
            mode = "RGBA"
        else:
            mode = None  # unknown

        # skip over blend flags and extra information
        read(12)  # filler
        name = ""
        size = i32(read(4))  # length of the extra data field
        combined = 0
        if size:
            data_end = fp.tell() + size

            length = i32(read(4))
            if length:
                fp.seek(length - 16, io.SEEK_CUR)
            combined += length + 4

            length = i32(read(4))
            if length:
                fp.seek(length, io.SEEK_CUR)
            combined += length + 4

            length = i8(read(1))
            if length:
                # Don't know the proper encoding,
                # Latin-1 should be a good guess
                name = read(length).decode("latin-1", "replace")
            combined += length + 1

            fp.seek(data_end)
        layers.append((name, mode, (x0, y0, x1, y1)))

    # get tiles
    i = 0
    for name, mode, bbox in layers:
        tile = []
        for m in mode:
            t = _maketile(fp, m, bbox, 1)
            if t:
                tile.extend(t)
        layers[i] = name, mode, bbox, tile
        i += 1

    return layers
