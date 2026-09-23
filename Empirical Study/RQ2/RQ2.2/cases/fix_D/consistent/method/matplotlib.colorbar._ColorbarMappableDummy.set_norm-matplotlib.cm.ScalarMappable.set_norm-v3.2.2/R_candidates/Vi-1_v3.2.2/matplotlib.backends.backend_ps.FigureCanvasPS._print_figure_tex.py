    @cbook._delete_parameter("3.2", "dryrun")
    def _print_figure_tex(
            self, outfile, format, dpi, facecolor, edgecolor,
            orientation, papertype, *,
            metadata=None, dryrun=False, bbox_inches_restore=None, **kwargs):
        """
        If text.usetex is True in rc, a temporary pair of tex/eps files
        are created to allow tex to manage the text layout via the PSFrags
        package. These files are processed to yield the final ps or eps file.

        metadata must be a dictionary. Currently, only the value for
        the key 'Creator' is used.
        """
        is_eps = format == 'eps'
        if is_writable_file_like(outfile):
            title = None
        else:
            try:
                title = os.fspath(outfile)
            except TypeError:
                raise ValueError(
                    "outfile must be a path or a file-like object")

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
            class NullWriter:
                def write(self, *args, **kwargs):
                    pass

            self._pswriter = NullWriter()
        else:
            self._pswriter = StringIO()

        # mixed mode rendering
        ps_renderer = RendererPS(width, height, self._pswriter, imagedpi=dpi)
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
            # get source date from SOURCE_DATE_EPOCH, if set
            # See https://reproducible-builds.org/specs/source-date-epoch/
            source_date_epoch = os.getenv("SOURCE_DATE_EPOCH")
            if source_date_epoch:
                source_date = datetime.datetime.utcfromtimestamp(
                    int(source_date_epoch)).strftime("%a %b %d %H:%M:%S %Y")
            else:
                source_date = time.ctime()
            pathlib.Path(tmpfile).write_text(
                f"""\
%!PS-Adobe-3.0 EPSF-3.0
{f'''%%Title: {title}
''' if title else ""}\
%%Creator: {creator_str}
%%CreationDate: {source_date}
%%BoundingBox: {bbox[0]} {bbox[1]} {bbox[2]} {bbox[3]}
%%EndComments
%%BeginProlog
/mpldict {len(psDefs)} dict def
mpldict begin
{"".join(psDefs)}
end
%%EndProlog
mpldict begin
{_nums_to_str(xo, yo)} translate
{_nums_to_str(width*72, height*72)} 0 0 clipbox
{self._pswriter.getvalue()}
end
showpage
""",
                encoding="latin-1")

            if orientation is _Orientation.landscape:  # now, ready to rotate
                width, height = height, width
                bbox = (lly, llx, ury, urx)

            # set the paper size to the figure size if is_eps. The
            # resulting ps file has the given size with correct bounding
            # box so that there is no need to call 'pstoeps'
            if is_eps:
                paper_width, paper_height = orientation.swap_if_landscape(
                    self.figure.get_size_inches())
            else:
                temp_papertype = _get_papertype(width, height)
                if papertype == 'auto':
                    papertype = temp_papertype
                    paper_width, paper_height = papersize[temp_papertype]
                else:
                    paper_width, paper_height = papersize[papertype]

            texmanager = ps_renderer.get_texmanager()
            font_preamble = texmanager.get_font_preamble()
            custom_preamble = texmanager.get_custom_preamble()

            psfrag_rotated = convert_psfrags(tmpfile, ps_renderer.psfrag,
                                             font_preamble,
                                             custom_preamble, paper_width,
                                             paper_height,
                                             orientation.name)

            if (rcParams['ps.usedistiller'] == 'ghostscript'
                    or rcParams['text.usetex']):
                gs_distill(tmpfile, is_eps, ptype=papertype, bbox=bbox,
                           rotated=psfrag_rotated)
            elif rcParams['ps.usedistiller'] == 'xpdf':
                xpdf_distill(tmpfile, is_eps, ptype=papertype, bbox=bbox,
                             rotated=psfrag_rotated)

            _move_path_to_path_or_stream(tmpfile, outfile)
