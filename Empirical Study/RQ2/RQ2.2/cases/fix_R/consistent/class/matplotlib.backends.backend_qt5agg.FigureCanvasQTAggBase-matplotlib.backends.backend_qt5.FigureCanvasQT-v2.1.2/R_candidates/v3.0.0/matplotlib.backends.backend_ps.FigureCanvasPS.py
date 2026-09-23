class FigureCanvasPS(FigureCanvasBase):
    _renderer_class = RendererPS

    fixed_dpi = 72

    def draw(self):
        pass

    filetypes = {'ps'  : 'Postscript',
                 'eps' : 'Encapsulated Postscript'}

    def get_default_filetype(self):
        return 'ps'

    def print_ps(self, outfile, *args, **kwargs):
        return self._print_ps(outfile, 'ps', *args, **kwargs)

    def print_eps(self, outfile, *args, **kwargs):
        return self._print_ps(outfile, 'eps', *args, **kwargs)

    def _print_ps(self, outfile, format, *args,
                  papertype=None, dpi=72, facecolor='w', edgecolor='w',
                  orientation='portrait',
                  **kwargs):
        if papertype is None:
            papertype = rcParams['ps.papersize']
        papertype = papertype.lower()
        if papertype == 'auto':
            pass
        elif papertype not in papersize:
            raise RuntimeError('%s is not a valid papertype. Use one of %s' %
                               (papertype, ', '.join(papersize)))

        orientation = orientation.lower()
        if orientation == 'landscape': isLandscape = True
        elif orientation == 'portrait': isLandscape = False
        else: raise RuntimeError('Orientation must be "portrait" or "landscape"')

        self.figure.set_dpi(72) # Override the dpi kwarg

        if rcParams['text.usetex']:
            self._print_figure_tex(outfile, format, dpi, facecolor, edgecolor,
                                   orientation, isLandscape, papertype,
                                   **kwargs)
        else:
            self._print_figure(outfile, format, dpi, facecolor, edgecolor,
                               orientation, isLandscape, papertype,
                               **kwargs)

    def _print_figure(
            self, outfile, format, dpi=72, facecolor='w', edgecolor='w',
            orientation='portrait', isLandscape=False, papertype=None,
            metadata=None, *,
            dryrun=False, bbox_inches_restore=None, **kwargs):
        """
        Render the figure to hardcopy.  Set the figure patch face and
        edge colors.  This is useful because some of the GUIs have a
        gray figure face color background and you'll probably want to
        override this on hardcopy

        If outfile is a string, it is interpreted as a file name.
        If the extension matches .ep* write encapsulated postscript,
        otherwise write a stand-alone PostScript file.

        If outfile is a file object, a stand-alone PostScript file is
        written into this file object.

        metadata must be a dictionary. Currently, only the value for
        the key 'Creator' is used.
        """
        isEPSF = format == 'eps'
        if isinstance(outfile, (str, getattr(os, "PathLike", ()),)):
            outfile = title = getattr(os, "fspath", lambda obj: obj)(outfile)
            title = title.encode("latin-1", "replace").decode()
            passed_in_file_object = False
        elif is_writable_file_like(outfile):
            title = None
            passed_in_file_object = True
        else:
            raise ValueError("outfile must be a path or a file-like object")

        # find the appropriate papertype
        width, height = self.figure.get_size_inches()
        if papertype == 'auto':
            if isLandscape: papertype = _get_papertype(height, width)
            else: papertype = _get_papertype(width, height)

        if isLandscape: paperHeight, paperWidth = papersize[papertype]
        else: paperWidth, paperHeight = papersize[papertype]

        if rcParams['ps.usedistiller'] and not papertype == 'auto':
            # distillers will improperly clip eps files if the pagesize is
            # too small
            if width>paperWidth or height>paperHeight:
                if isLandscape:
                    papertype = _get_papertype(height, width)
                    paperHeight, paperWidth = papersize[papertype]
                else:
                    papertype = _get_papertype(width, height)
                    paperWidth, paperHeight = papersize[papertype]

        # center the figure on the paper
        xo = 72*0.5*(paperWidth - width)
        yo = 72*0.5*(paperHeight - height)

        l, b, w, h = self.figure.bbox.bounds
        llx = xo
        lly = yo
        urx = llx + w
        ury = lly + h
        rotation = 0
        if isLandscape:
            llx, lly, urx, ury = lly, llx, ury, urx
            xo, yo = 72*paperHeight - yo, xo
            rotation = 90
        bbox = (llx, lly, urx, ury)

        # generate PostScript code for the figure and store it in a string
        origfacecolor = self.figure.get_facecolor()
        origedgecolor = self.figure.get_edgecolor()
        self.figure.set_facecolor(facecolor)
        self.figure.set_edgecolor(edgecolor)

        if dryrun:
            class NullWriter(object):
                def write(self, *kl, **kwargs):
                    pass

            self._pswriter = NullWriter()
        else:
            self._pswriter = StringIO()

        # mixed mode rendering
        ps_renderer = self._renderer_class(width, height, self._pswriter,
                                           imagedpi=dpi)
        renderer = MixedModeRenderer(self.figure,
            width, height, dpi, ps_renderer,
            bbox_inches_restore=bbox_inches_restore)

        self.figure.draw(renderer)

        if dryrun: # return immediately if dryrun (tightbbox=True)
            return

        self.figure.set_facecolor(origfacecolor)
        self.figure.set_edgecolor(origedgecolor)

        # check for custom metadata
        if metadata is not None and 'Creator' in metadata:
            creator_str = metadata['Creator']
        else:
            creator_str = "matplotlib version " + __version__ + \
                ", http://matplotlib.org/"

        def print_figure_impl(fh):
            # write the PostScript headers
            if isEPSF:
                print("%!PS-Adobe-3.0 EPSF-3.0", file=fh)
            else:
                print("%!PS-Adobe-3.0", file=fh)
            if title:
                print("%%Title: " + title, file=fh)
            print("%%Creator: " + creator_str, file=fh)
            # get source date from SOURCE_DATE_EPOCH, if set
            # See https://reproducible-builds.org/specs/source-date-epoch/
            source_date_epoch = os.getenv("SOURCE_DATE_EPOCH")
            if source_date_epoch:
                source_date = datetime.datetime.utcfromtimestamp(
                    int(source_date_epoch)).strftime("%a %b %d %H:%M:%S %Y")
            else:
                source_date = time.ctime()
            print("%%CreationDate: " + source_date, file=fh)
            print("%%Orientation: " + orientation, file=fh)
            if not isEPSF:
                print("%%DocumentPaperSizes: "+papertype, file=fh)
            print("%%%%BoundingBox: %d %d %d %d" % bbox, file=fh)
            if not isEPSF:
                print("%%Pages: 1", file=fh)
            print("%%EndComments", file=fh)

            Ndict = len(psDefs)
            print("%%BeginProlog", file=fh)
            if not rcParams['ps.useafm']:
                Ndict += len(ps_renderer.used_characters)
            print("/mpldict %d dict def" % Ndict, file=fh)
            print("mpldict begin", file=fh)
            for d in psDefs:
                d = d.strip()
                for l in d.split('\n'):
                    print(l.strip(), file=fh)
            if not rcParams['ps.useafm']:
                for font_filename, chars in \
                        ps_renderer.used_characters.values():
                    if len(chars):
                        font = get_font(font_filename)
                        glyph_ids = []
                        for c in chars:
                            gind = font.get_char_index(c)
                            glyph_ids.append(gind)

                        fonttype = rcParams['ps.fonttype']

                        # Can not use more than 255 characters from a
                        # single font for Type 3
                        if len(glyph_ids) > 255:
                            fonttype = 42

                        # The ttf to ps (subsetting) support doesn't work for
                        # OpenType fonts that are Postscript inside (like the
                        # STIX fonts).  This will simply turn that off to avoid
                        # errors.
                        if is_opentype_cff_font(font_filename):
                            raise RuntimeError(
                                "OpenType CFF fonts can not be saved using "
                                "the internal Postscript backend at this "
                                "time; consider using the Cairo backend")
                        else:
                            fh.flush()
                            convert_ttf_to_ps(os.fsencode(font_filename),
                                              fh, fonttype, glyph_ids)
            print("end", file=fh)
            print("%%EndProlog", file=fh)

            if not isEPSF:
                print("%%Page: 1 1", file=fh)
            print("mpldict begin", file=fh)

            print("%s translate" % _nums_to_str(xo, yo), file=fh)
            if rotation:
                print("%d rotate" % rotation, file=fh)
            print("%s clipbox" % _nums_to_str(width*72, height*72, 0, 0),
                  file=fh)

            # write the figure
            content = self._pswriter.getvalue()
            if not isinstance(content, str):
                content = content.decode('ascii')
            print(content, file=fh)

            # write the trailer
            print("end", file=fh)
            print("showpage", file=fh)
            if not isEPSF:
                print("%%EOF", file=fh)
            fh.flush()

        if rcParams['ps.usedistiller']:
            # We are going to use an external program to process the output.
            # Write to a temporary file.
            with TemporaryDirectory() as tmpdir:
                tmpfile = os.path.join(tmpdir, "tmp.ps")
                with open(tmpfile, 'w', encoding='latin-1') as fh:
                    print_figure_impl(fh)
                if rcParams['ps.usedistiller'] == 'ghostscript':
                    gs_distill(tmpfile, isEPSF, ptype=papertype, bbox=bbox)
                elif rcParams['ps.usedistiller'] == 'xpdf':
                    xpdf_distill(tmpfile, isEPSF, ptype=papertype, bbox=bbox)
                _move_path_to_path_or_stream(tmpfile, outfile)

        else:
            # Write directly to outfile.
            if passed_in_file_object:
                requires_unicode = file_requires_unicode(outfile)

                if not requires_unicode:
                    fh = TextIOWrapper(outfile, encoding="latin-1")
                    # Prevent the TextIOWrapper from closing the underlying
                    # file.
                    def do_nothing():
                        pass
                    fh.close = do_nothing
                else:
                    fh = outfile

                print_figure_impl(fh)
            else:
                with open(outfile, 'w', encoding='latin-1') as fh:
                    print_figure_impl(fh)

    def _print_figure_tex(
            self, outfile, format, dpi, facecolor, edgecolor,
            orientation, isLandscape, papertype, metadata=None, *,
            dryrun=False, bbox_inches_restore=None, **kwargs):
        """
        If text.usetex is True in rc, a temporary pair of tex/eps files
        are created to allow tex to manage the text layout via the PSFrags
        package. These files are processed to yield the final ps or eps file.

        metadata must be a dictionary. Currently, only the value for
        the key 'Creator' is used.
        """
        isEPSF = format == 'eps'
        if isinstance(outfile, str):
            title = outfile
        elif is_writable_file_like(outfile):
            title = None
        else:
            raise ValueError("outfile must be a path or a file-like object")

        self.figure.dpi = 72  # ignore the dpi kwarg
        width, height = self.figure.get_size_inches()
        xo = 0
        yo = 0

        l, b, w, h = self.figure.bbox.bounds
        llx = xo
        lly = yo
        urx = llx + w
        ury = lly + h
        bbox = (llx, lly, urx, ury)

        # generate PostScript code for the figure and store it in a string
        origfacecolor = self.figure.get_facecolor()
        origedgecolor = self.figure.get_edgecolor()
        self.figure.set_facecolor(facecolor)
        self.figure.set_edgecolor(edgecolor)

        if dryrun:
            class NullWriter(object):
                def write(self, *kl, **kwargs):
                    pass

            self._pswriter = NullWriter()
        else:
            self._pswriter = StringIO()

        # mixed mode rendering
        ps_renderer = self._renderer_class(width, height,
                                           self._pswriter, imagedpi=dpi)
        renderer = MixedModeRenderer(self.figure,
                                     width, height, dpi, ps_renderer,
                                     bbox_inches_restore=bbox_inches_restore)

        self.figure.draw(renderer)

        if dryrun:  # return immediately if dryrun (tightbbox=True)
            return

        self.figure.set_facecolor(origfacecolor)
        self.figure.set_edgecolor(origedgecolor)

        # check for custom metadata
        if metadata is not None and 'Creator' in metadata:
            creator_str = metadata['Creator']
        else:
            creator_str = "matplotlib version " + __version__ + \
                ", http://matplotlib.org/"

        # write to a temp file, we'll move it to outfile when done

        with TemporaryDirectory() as tmpdir:
            tmpfile = os.path.join(tmpdir, "tmp.ps")
            with open(tmpfile, 'w', encoding='latin-1') as fh:
                # write the Encapsulated PostScript headers
                print("%!PS-Adobe-3.0 EPSF-3.0", file=fh)
                if title:
                    print("%%Title: "+title, file=fh)
                print("%%Creator: " + creator_str, file=fh)
                # get source date from SOURCE_DATE_EPOCH, if set
                # See https://reproducible-builds.org/specs/source-date-epoch/
                source_date_epoch = os.getenv("SOURCE_DATE_EPOCH")
                if source_date_epoch:
                    source_date = datetime.datetime.utcfromtimestamp(
                        int(source_date_epoch)).strftime(
                            "%a %b %d %H:%M:%S %Y")
                else:
                    source_date = time.ctime()
                print("%%CreationDate: "+source_date, file=fh)
                print("%%%%BoundingBox: %d %d %d %d" % bbox, file=fh)
                print("%%EndComments", file=fh)

                Ndict = len(psDefs)
                print("%%BeginProlog", file=fh)
                print("/mpldict %d dict def" % Ndict, file=fh)
                print("mpldict begin", file=fh)
                for d in psDefs:
                    d = d.strip()
                    for l in d.split('\n'):
                        print(l.strip(), file=fh)
                print("end", file=fh)
                print("%%EndProlog", file=fh)

                print("mpldict begin", file=fh)
                print("%s translate" % _nums_to_str(xo, yo), file=fh)
                print("%s clipbox" % _nums_to_str(width*72, height*72, 0, 0),
                      file=fh)

                # write the figure
                print(self._pswriter.getvalue(), file=fh)

                # write the trailer
                print("end", file=fh)
                print("showpage", file=fh)
                fh.flush()

            if isLandscape:  # now we are ready to rotate
                isLandscape = True
                width, height = height, width
                bbox = (lly, llx, ury, urx)

            # set the paper size to the figure size if isEPSF. The
            # resulting ps file has the given size with correct bounding
            # box so that there is no need to call 'pstoeps'
            if isEPSF:
                paperWidth, paperHeight = self.figure.get_size_inches()
                if isLandscape:
                    paperWidth, paperHeight = paperHeight, paperWidth
            else:
                temp_papertype = _get_papertype(width, height)
                if papertype == 'auto':
                    papertype = temp_papertype
                    paperWidth, paperHeight = papersize[temp_papertype]
                else:
                    paperWidth, paperHeight = papersize[papertype]
                    if (width > paperWidth or height > paperHeight) and isEPSF:
                        paperWidth, paperHeight = papersize[temp_papertype]
                        _log.info('Your figure is too big to fit on %s paper. '
                                  '%s paper will be used to prevent clipping.',
                                  papertype, temp_papertype)

            texmanager = ps_renderer.get_texmanager()
            font_preamble = texmanager.get_font_preamble()
            custom_preamble = texmanager.get_custom_preamble()

            psfrag_rotated = convert_psfrags(tmpfile, ps_renderer.psfrag,
                                             font_preamble,
                                             custom_preamble, paperWidth,
                                             paperHeight,
                                             orientation)

            if (rcParams['ps.usedistiller'] == 'ghostscript'
                    or rcParams['text.usetex']):
                gs_distill(tmpfile, isEPSF, ptype=papertype, bbox=bbox,
                           rotated=psfrag_rotated)
            elif rcParams['ps.usedistiller'] == 'xpdf':
                xpdf_distill(tmpfile, isEPSF, ptype=papertype, bbox=bbox,
                             rotated=psfrag_rotated)

            _move_path_to_path_or_stream(tmpfile, outfile)
