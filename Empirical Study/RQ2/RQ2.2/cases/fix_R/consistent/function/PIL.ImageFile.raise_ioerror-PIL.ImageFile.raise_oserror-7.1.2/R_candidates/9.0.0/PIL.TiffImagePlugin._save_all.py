def _save_all(im, fp, filename):
    encoderinfo = im.encoderinfo.copy()
    encoderconfig = im.encoderconfig
    append_images = list(encoderinfo.get("append_images", []))
    if not hasattr(im, "n_frames") and not append_images:
        return _save(im, fp, filename)

    cur_idx = im.tell()
    try:
        with AppendingTiffWriter(fp) as tf:
            for ims in [im] + append_images:
                ims.encoderinfo = encoderinfo
                ims.encoderconfig = encoderconfig
                if not hasattr(ims, "n_frames"):
                    nfr = 1
                else:
                    nfr = ims.n_frames

                for idx in range(nfr):
                    ims.seek(idx)
                    ims.load()
                    _save(ims, tf, filename)
                    tf.newFrame()
    finally:
        im.seek(cur_idx)
