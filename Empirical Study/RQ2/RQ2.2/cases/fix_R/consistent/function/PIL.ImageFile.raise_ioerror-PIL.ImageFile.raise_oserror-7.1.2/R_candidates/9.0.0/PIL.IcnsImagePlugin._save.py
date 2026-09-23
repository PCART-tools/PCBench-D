def _save(im, fp, filename):
    """
    Saves the image as a series of PNG files,
    that are then combined into a .icns file.
    """
    if hasattr(fp, "flush"):
        fp.flush()

    sizes = {
        b"ic07": 128,
        b"ic08": 256,
        b"ic09": 512,
        b"ic10": 1024,
        b"ic11": 32,
        b"ic12": 64,
        b"ic13": 256,
        b"ic14": 512,
    }
    provided_images = {im.width: im for im in im.encoderinfo.get("append_images", [])}
    size_streams = {}
    for size in set(sizes.values()):
        image = (
            provided_images[size]
            if size in provided_images
            else im.resize((size, size))
        )

        temp = io.BytesIO()
        image.save(temp, "png")
        size_streams[size] = temp.getvalue()

    entries = []
    for type, size in sizes.items():
        stream = size_streams[size]
        entries.append(
            {"type": type, "size": HEADERSIZE + len(stream), "stream": stream}
        )

    # Header
    fp.write(MAGIC)
    file_length = HEADERSIZE  # Header
    file_length += HEADERSIZE + 8 * len(entries)  # TOC
    file_length += sum(entry["size"] for entry in entries)
    fp.write(struct.pack(">i", file_length))

    # TOC
    fp.write(b"TOC ")
    fp.write(struct.pack(">i", HEADERSIZE + len(entries) * HEADERSIZE))
    for entry in entries:
        fp.write(entry["type"])
        fp.write(struct.pack(">i", entry["size"]))

    # Data
    for entry in entries:
        fp.write(entry["type"])
        fp.write(struct.pack(">i", entry["size"]))
        fp.write(entry["stream"])

    if hasattr(fp, "flush"):
        fp.flush()
