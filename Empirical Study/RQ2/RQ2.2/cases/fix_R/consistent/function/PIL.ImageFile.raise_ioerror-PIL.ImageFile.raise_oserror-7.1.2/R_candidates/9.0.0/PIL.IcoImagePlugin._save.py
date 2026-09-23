def _save(im, fp, filename):
    fp.write(_MAGIC)  # (2+2)
    sizes = im.encoderinfo.get(
        "sizes",
        [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)],
    )
    width, height = im.size
    sizes = filter(
        lambda x: False
        if (x[0] > width or x[1] > height or x[0] > 256 or x[1] > 256)
        else True,
        sizes,
    )
    sizes = list(sizes)
    fp.write(struct.pack("<H", len(sizes)))  # idCount(2)
    offset = fp.tell() + len(sizes) * 16
    bmp = im.encoderinfo.get("bitmap_format") == "bmp"
    provided_images = {im.size: im for im in im.encoderinfo.get("append_images", [])}
    for size in sizes:
        width, height = size
        # 0 means 256
        fp.write(struct.pack("B", width if width < 256 else 0))  # bWidth(1)
        fp.write(struct.pack("B", height if height < 256 else 0))  # bHeight(1)
        fp.write(b"\0")  # bColorCount(1)
        fp.write(b"\0")  # bReserved(1)
        fp.write(b"\0\0")  # wPlanes(2)

        tmp = provided_images.get(size)
        if not tmp:
            # TODO: invent a more convenient method for proportional scalings
            tmp = im.copy()
            tmp.thumbnail(size, Image.LANCZOS, reducing_gap=None)
        bits = BmpImagePlugin.SAVE[tmp.mode][1] if bmp else 32
        fp.write(struct.pack("<H", bits))  # wBitCount(2)

        image_io = BytesIO()
        if bmp:
            tmp.save(image_io, "dib")

            if bits != 32:
                and_mask = Image.new("1", tmp.size)
                ImageFile._save(
                    and_mask, image_io, [("raw", (0, 0) + tmp.size, 0, ("1", 0, -1))]
                )
        else:
            tmp.save(image_io, "png")
        image_io.seek(0)
        image_bytes = image_io.read()
        if bmp:
            image_bytes = image_bytes[:8] + o32(height * 2) + image_bytes[12:]
        bytes_len = len(image_bytes)
        fp.write(struct.pack("<I", bytes_len))  # dwBytesInRes(4)
        fp.write(struct.pack("<I", offset))  # dwImageOffset(4)
        current = fp.tell()
        fp.seek(offset)
        fp.write(image_bytes)
        offset = offset + bytes_len
        fp.seek(current)
