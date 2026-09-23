def _save(im, fp, filename, save_all=False):
    # header
    if "palette" in im.encoderinfo or "palette" in im.info:
        palette = im.encoderinfo.get("palette", im.info.get("palette"))
    else:
        palette = None
        im.encoderinfo["optimize"] = im.encoderinfo.get("optimize", True)

    if not save_all or not _write_multiple_frames(im, fp, palette):
        _write_single_frame(im, fp, palette)

    fp.write(b";")  # end of file

    if hasattr(fp, "flush"):
        fp.flush()
