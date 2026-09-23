    @_check_savefig_extra_args
    @cbook._delete_parameter("3.2", "dryrun")
    def _print_figure(
            self, outfile, format, *,
            dpi, dsc_comments, orientation, papertype,
            dryrun=False, bbox_inches_restore=None):
        """
        Render the figure to a filesystem path or a file-like object.

        Parameters are as for `.print_figure`, except that *dsc_comments* is a
        all string containing Document Structuring Convention comments,
        generated from the *metadata* parameter to `.print_figure`.
        """
        is_eps = format == 'eps'
        if isinstance(outfile, (str, os.PathLike)):
            outfile = os.fspath(outfile)
            passed_in_file_object = False
        elif is_writable_file_like(outfile):
            passed_in_file_object = True
        else:
            raise ValueError("outfile must be a path or a file-like object")

        # find the appropriate papertype
        width, height = self.figure.get_size_inches()
        if papertype == 'auto':
            papertype = _get_papertype(
                *orientation.swap_if_landscape((width, height)))
        paper_width, paper_height = orientation.swap_if_landscape(
            papersize[papertype])

        if mpl.rcParams['ps.usedistiller']:
            # distillers improperly clip eps files if pagesize is too small
            if width > paper_width or height > paper_height:
                papertype = _get_papertype(
                    *orientation.swap_if_landscape(width, height))
                paper_width, paper_height = orientation.swap_if_landscape(
                    papersize[papertype])

        # center the figure on the paper
        xo = 72 * 0.5 * (paper_width - width)
        yo = 72 * 0.5 * (paper_height - height)

        llx = xo
        lly = yo
        urx = llx + self.figure.bbox.width
        ury = lly + self.figure.bbox.height
        rotation = 0
        if orientation is _Orientation.landscape:
            llx, lly, urx, ury = lly, llx, ury, urx
            xo, yo = 72 * paper_height - yo, xo
            rotation = 90
        bbox = (llx, lly, urx, ury)

        if dryrun:
            class NullWriter:
                def write(self, *args, **kwargs):
                    pass

            self._pswriter = NullWriter()
        else:
            self._pswriter = StringIO()

        # mixed mode rendering
        ps_renderer = RendererPS(width, height, self._pswriter, imagedpi=dpi)
        renderer = MixedModeRenderer(
            self.figure, width, height, dpi, ps_renderer,
            bbox_inches_restore=bbox_inches_restore)

        self.figure.draw(renderer)

        if dryrun:  # return immediately if dryrun (tightbbox=True)
            return

        def print_figure_impl(fh):
            # write the PostScript headers
            if is_eps:
                print("%!PS-Adobe-3.0 EPSF-3.0", file=fh)
            else:
                print(f"%!PS-Adobe-3.0\n"
                      f"%%DocumentPaperSizes: {papertype}\n"
                      f"%%Pages: 1\n",
                      end="", file=fh)
            print(f"{dsc_comments}\n"
                  f"%%Orientation: {orientation.name}\n"
                  f"%%BoundingBox: {bbox[0]} {bbox[1]} {bbox[2]} {bbox[3]}\n"
                  f"%%EndComments\n",
                  end="", file=fh)

            Ndict = len(psDefs)
            print("%%BeginProlog", file=fh)
            if not mpl.rcParams['ps.useafm']:
                Ndict += len(ps_renderer._character_tracker.used)
            print("/mpldict %d dict def" % Ndict, file=fh)
            print("mpldict begin", file=fh)
            print("\n".join(psDefs), file=fh)
            if not mpl.rcParams['ps.useafm']:
                for font_path, chars \
                        in ps_renderer._character_tracker.used.items():
                    if not chars:
                        continue
                    font = get_font(font_path)
                    glyph_ids = [font.get_char_index(c) for c in chars]
                    fonttype = mpl.rcParams['ps.fonttype']
                    # Can't use more than 255 chars from a single Type 3 font.
                    if len(glyph_ids) > 255:
                        fonttype = 42
                    # The ttf to ps (subsetting) support doesn't work for
                    # OpenType fonts that are Postscript inside (like the STIX
                    # fonts).  This will simply turn that off to avoid errors.
                    if is_opentype_cff_font(font_path):
                        raise RuntimeError(
                            "OpenType CFF fonts can not be saved using "
                            "the internal Postscript backend at this "
                            "time; consider using the Cairo backend")
                    fh.flush()
                    try:
                        convert_ttf_to_ps(os.fsencode(font_path),
                                          fh, fonttype, glyph_ids)
                    except RuntimeError:
                        _log.warning("The PostScript backend does not "
                                     "currently support the selected font.")
                        raise
            print("end", file=fh)
            print("%%EndProlog", file=fh)

            if not is_eps:
                print("%%Page: 1 1", file=fh)
            print("mpldict begin", file=fh)

            print("%s translate" % _nums_to_str(xo, yo), file=fh)
            if rotation:
                print("%d rotate" % rotation, file=fh)
            print("%s clipbox" % _nums_to_str(width*72, height*72, 0, 0),
                  file=fh)

            # write the figure
            print(self._pswriter.getvalue(), file=fh)

            # write the trailer
            print("end", file=fh)
            print("showpage", file=fh)
            if not is_eps:
                print("%%EOF", file=fh)
            fh.flush()

        if mpl.rcParams['ps.usedistiller']:
            # We are going to use an external program to process the output.
            # Write to a temporary file.
            with TemporaryDirectory() as tmpdir:
                tmpfile = os.path.join(tmpdir, "tmp.ps")
                with open(tmpfile, 'w', encoding='latin-1') as fh:
                    print_figure_impl(fh)
                if mpl.rcParams['ps.usedistiller'] == 'ghostscript':
                    _try_distill(gs_distill,
                                 tmpfile, is_eps, ptype=papertype, bbox=bbox)
                elif mpl.rcParams['ps.usedistiller'] == 'xpdf':
                    _try_distill(xpdf_distill,
                                 tmpfile, is_eps, ptype=papertype, bbox=bbox)
                _move_path_to_path_or_stream(tmpfile, outfile)

        else:
            # Write directly to outfile.
            if passed_in_file_object:
                requires_unicode = file_requires_unicode(outfile)

                if not requires_unicode:
                    fh = TextIOWrapper(outfile, encoding="latin-1")
                    # Prevent the TextIOWrapper from closing the underlying
                    # file.
                    fh.close = lambda: None
                else:
                    fh = outfile

                print_figure_impl(fh)
            else:
                with open(outfile, 'w', encoding='latin-1') as fh:
                    print_figure_impl(fh)
