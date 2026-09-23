def _write(out_path, text):
    old_text: Optional[str]
    try:
        with open(out_path) as f:
            old_text = f.read()
    except OSError:
        old_text = None
    if old_text != text:
        with open(out_path, "w") as f:
            logger.info("Writing %s", out_path)
            f.write(text)
    else:
        logger.info("Skipped writing %s", out_path)
