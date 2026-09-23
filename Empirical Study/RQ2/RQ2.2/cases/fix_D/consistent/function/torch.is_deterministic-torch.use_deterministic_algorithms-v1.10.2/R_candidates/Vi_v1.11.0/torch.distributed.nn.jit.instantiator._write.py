def _write(out_path, text):
    old_text: Optional[str]
    try:
        with open(out_path, "r") as f:
            old_text = f.read()
    except IOError:
        old_text = None
    if old_text != text:
        with open(out_path, "w") as f:
            logger.info("Writing {}".format(out_path))
            f.write(text)
    else:
        logger.info("Skipped writing {}".format(out_path))
