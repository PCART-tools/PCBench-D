def _save(im, fp, filename):

    if im.mode != "1":
        raise OSError(f"cannot write mode {im.mode} as XBM")

    fp.write(f"#define im_width {im.size[0]}\n".encode("ascii"))
    fp.write(f"#define im_height {im.size[1]}\n".encode("ascii"))

    hotspot = im.encoderinfo.get("hotspot")
    if hotspot:
        fp.write(f"#define im_x_hot {hotspot[0]}\n".encode("ascii"))
        fp.write(f"#define im_y_hot {hotspot[1]}\n".encode("ascii"))

    fp.write(b"static char im_bits[] = {\n")

    ImageFile._save(im, fp, [("xbm", (0, 0) + im.size, 0, None)])

    fp.write(b"};\n")
