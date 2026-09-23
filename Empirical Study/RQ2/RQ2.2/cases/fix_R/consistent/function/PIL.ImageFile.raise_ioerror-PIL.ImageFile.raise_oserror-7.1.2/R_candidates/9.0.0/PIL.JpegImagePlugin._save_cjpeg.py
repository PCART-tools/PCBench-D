def _save_cjpeg(im, fp, filename):
    # ALTERNATIVE: handle JPEGs via the IJG command line utilities.
    tempfile = im._dump()
    subprocess.check_call(["cjpeg", "-outfile", filename, tempfile])
    try:
        os.unlink(tempfile)
    except OSError:
        pass
