def xpdf_distill(tmpfile, eps=False, ptype='letter', bbox=None, rotated=False):
    """
    Use ghostscript's ps2pdf and xpdf's/poppler's pdftops to distill a file.
    This yields smaller files without illegal encapsulated postscript
    operators. This distiller is preferred, generating high-level postscript
    output that treats text as text.
    """
    mpl._get_executable_info("gs")  # Effectively checks for ps2pdf.
    mpl._get_executable_info("pdftops")

    pdffile = tmpfile + '.pdf'
    psfile = tmpfile + '.ps'

    # Pass options as `-foo#bar` instead of `-foo=bar` to keep Windows happy
    # (https://www.ghostscript.com/doc/9.22/Use.htm#MS_Windows).
    cbook._check_and_log_subprocess(
        ["ps2pdf",
         "-dAutoFilterColorImages#false",
         "-dAutoFilterGrayImages#false",
         "-sAutoRotatePages#None",
         "-sGrayImageFilter#FlateEncode",
         "-sColorImageFilter#FlateEncode",
         "-dEPSCrop" if eps else "-sPAPERSIZE#%s" % ptype,
         tmpfile, pdffile], _log)
    cbook._check_and_log_subprocess(
        ["pdftops", "-paper", "match", "-level2", pdffile, psfile], _log)

    os.remove(tmpfile)
    shutil.move(psfile, tmpfile)

    if eps:
        pstoeps(tmpfile)

    for fname in glob.glob(tmpfile+'.*'):
        os.remove(fname)
