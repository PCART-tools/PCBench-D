def _save(im, fp, filename):
    if im.mode[0] != "F":
        im = im.convert("F")

    hdr = makeSpiderHeader(im)
    if len(hdr) < 256:
        raise OSError("Error creating Spider header")

    # write the SPIDER header
    fp.writelines(hdr)

    rawmode = "F;32NF"  # 32-bit native floating point
    ImageFile._save(im, fp, [("raw", (0, 0) + im.size, 0, (rawmode, 0, 1))])
