def make_pdf_to_png_converter():
    """Return a function that converts a pdf file to a png file."""
    if shutil.which("pdftocairo"):
        def cairo_convert(pdffile, pngfile, dpi):
            cmd = ["pdftocairo", "-singlefile", "-png", "-r", "%d" % dpi,
                   pdffile, os.path.splitext(pngfile)[0]]
            subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        return cairo_convert
    try:
        gs_info = mpl._get_executable_info("gs")
    except mpl.ExecutableNotFoundError:
        pass
    else:
        def gs_convert(pdffile, pngfile, dpi):
            cmd = [gs_info.executable,
                   '-dQUIET', '-dSAFER', '-dBATCH', '-dNOPAUSE', '-dNOPROMPT',
                   '-dUseCIEColor', '-dTextAlphaBits=4',
                   '-dGraphicsAlphaBits=4', '-dDOINTERPOLATE',
                   '-sDEVICE=png16m', '-sOutputFile=%s' % pngfile,
                   '-r%d' % dpi, pdffile]
            subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        return gs_convert
    raise RuntimeError("No suitable pdf to png renderer found.")
