def truetype(font=None, size=10, index=0, encoding="", layout_engine=None):
    """
    Load a TrueType or OpenType font from a file or file-like object,
    and create a font object.
    This function loads a font object from the given file or file-like
    object, and creates a font object for a font of the given size.

    Pillow uses FreeType to open font files. If you are opening many fonts
    simultaneously on Windows, be aware that Windows limits the number of files
    that can be open in C at once to 512. If you approach that limit, an
    ``OSError`` may be thrown, reporting that FreeType "cannot open resource".

    This function requires the _imagingft service.

    :param font: A filename or file-like object containing a TrueType font.
                 If the file is not found in this filename, the loader may also
                 search in other directories, such as the :file:`fonts/`
                 directory on Windows or :file:`/Library/Fonts/`,
                 :file:`/System/Library/Fonts/` and :file:`~/Library/Fonts/` on
                 macOS.

    :param size: The requested size, in points.
    :param index: Which font face to load (default is first available face).
    :param encoding: Which font encoding to use (default is Unicode). Possible
                     encodings include (see the FreeType documentation for more
                     information):

                     * "unic" (Unicode)
                     * "symb" (Microsoft Symbol)
                     * "ADOB" (Adobe Standard)
                     * "ADBE" (Adobe Expert)
                     * "ADBC" (Adobe Custom)
                     * "armn" (Apple Roman)
                     * "sjis" (Shift JIS)
                     * "gb  " (PRC)
                     * "big5"
                     * "wans" (Extended Wansung)
                     * "joha" (Johab)
                     * "lat1" (Latin-1)

                     This specifies the character set to use. It does not alter the
                     encoding of any text provided in subsequent operations.
    :param layout_engine: Which layout engine to use, if available:
                     :data:`.ImageFont.LAYOUT_BASIC` or :data:`.ImageFont.LAYOUT_RAQM`.

                     You can check support for Raqm layout using
                     :py:func:`PIL.features.check_feature` with ``feature="raqm"``.

                     .. versionadded:: 4.2.0
    :return: A font object.
    :exception OSError: If the file could not be read.
    """

    def freetype(font):
        return FreeTypeFont(font, size, index, encoding, layout_engine)

    try:
        return freetype(font)
    except OSError:
        if not isPath(font):
            raise
        ttf_filename = os.path.basename(font)

        dirs = []
        if sys.platform == "win32":
            # check the windows font repository
            # NOTE: must use uppercase WINDIR, to work around bugs in
            # 1.5.2's os.environ.get()
            windir = os.environ.get("WINDIR")
            if windir:
                dirs.append(os.path.join(windir, "fonts"))
        elif sys.platform in ("linux", "linux2"):
            lindirs = os.environ.get("XDG_DATA_DIRS", "")
            if not lindirs:
                # According to the freedesktop spec, XDG_DATA_DIRS should
                # default to /usr/share
                lindirs = "/usr/share"
            dirs += [os.path.join(lindir, "fonts") for lindir in lindirs.split(":")]
        elif sys.platform == "darwin":
            dirs += [
                "/Library/Fonts",
                "/System/Library/Fonts",
                os.path.expanduser("~/Library/Fonts"),
            ]

        ext = os.path.splitext(ttf_filename)[1]
        first_font_with_a_different_extension = None
        for directory in dirs:
            for walkroot, walkdir, walkfilenames in os.walk(directory):
                for walkfilename in walkfilenames:
                    if ext and walkfilename == ttf_filename:
                        return freetype(os.path.join(walkroot, walkfilename))
                    elif not ext and os.path.splitext(walkfilename)[0] == ttf_filename:
                        fontpath = os.path.join(walkroot, walkfilename)
                        if os.path.splitext(fontpath)[1] == ".ttf":
                            return freetype(fontpath)
                        if not ext and first_font_with_a_different_extension is None:
                            first_font_with_a_different_extension = fontpath
        if first_font_with_a_different_extension:
            return freetype(first_font_with_a_different_extension)
        raise
