def _get_global_header(im, info):
    """Return a list of strings representing a GIF header"""

    # Header Block
    # https://www.matthewflickinger.com/lab/whatsinagif/bits_and_bytes.asp

    version = b"87a"
    for extensionKey in ["transparency", "duration", "loop", "comment"]:
        if info and extensionKey in info:
            if (extensionKey == "duration" and info[extensionKey] == 0) or (
                extensionKey == "comment" and not (1 <= len(info[extensionKey]) <= 255)
            ):
                continue
            version = b"89a"
            break
    else:
        if im.info.get("version") == b"89a":
            version = b"89a"

    background = _get_background(im, info.get("background"))

    palette_bytes = _get_palette_bytes(im)
    color_table_size = _get_color_table_size(palette_bytes)

    return [
        b"GIF"  # signature
        + version  # version
        + o16(im.size[0])  # canvas width
        + o16(im.size[1]),  # canvas height
        # Logical Screen Descriptor
        # size of global color table + global color table flag
        o8(color_table_size + 128),  # packed fields
        # background + reserved/aspect
        o8(background) + o8(0),
        # Global Color Table
        _get_header_palette(palette_bytes),
    ]
