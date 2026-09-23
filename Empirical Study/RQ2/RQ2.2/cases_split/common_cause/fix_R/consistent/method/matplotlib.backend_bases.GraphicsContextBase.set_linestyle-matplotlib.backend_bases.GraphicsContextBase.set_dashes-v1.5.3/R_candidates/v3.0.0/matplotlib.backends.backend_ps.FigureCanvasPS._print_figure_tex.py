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
