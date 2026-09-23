    def _print_figure_tex(
            self, fmt, outfile, *,
            dpi, dsc_comments, orientation, papertype,
            bbox_inches_restore=None):
        """
        If :rc:`text.usetex` is True, a temporary pair of tex/eps files
        are created to allow tex to manage the text layout via the PSFrags
        package. These files are processed to yield the final ps or eps file.

        The rest of the behavior is as for `._print_figure`.
        """
        is_eps = fmt == 'eps'

        width, height = self.figure.get_size_inches()
        xo = 0
        yo = 0

        llx = xo
        lly = yo
        urx = llx + self.figure.bbox.width
        ury = lly + self.figure.bbox.height
        bbox = (llx, lly, urx, ury)

        self._pswriter = StringIO()

        # mixed mode rendering
        ps_renderer = RendererPS(width, height, self._pswriter, imagedpi=dpi)
        renderer = MixedModeRenderer(self.figure,
                                     width, height, dpi, ps_renderer,
                                     bbox_inches_restore=bbox_inches_restore)

        self.figure.draw(renderer)

        # write to a temp file, we'll move it to outfile when done
        with TemporaryDirectory() as tmpdir:
            tmppath = pathlib.Path(tmpdir, "tmp.ps")
            tmppath.write_text(
                f"""\
%!PS-Adobe-3.0 EPSF-3.0
%%LanguageLevel: 3
{dsc_comments}
{get_bbox_header(bbox)[0]}
%%EndComments
%%BeginProlog
/mpldict {len(_psDefs)} dict def
mpldict begin
{"".join(_psDefs)}
end
%%EndProlog
mpldict begin
{_nums_to_str(xo, yo)} translate
0 0 {_nums_to_str(width*72, height*72)} rectclip
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
            if is_eps or papertype == 'figure':
                paper_width, paper_height = orientation.swap_if_landscape(
                    self.figure.get_size_inches())
            else:
                if papertype == 'auto':
                    papertype = _get_papertype(width, height)
                paper_width, paper_height = papersize[papertype]

            psfrag_rotated = _convert_psfrags(
                tmppath, ps_renderer.psfrag, paper_width, paper_height,
                orientation.name)

            if (mpl.rcParams['ps.usedistiller'] == 'ghostscript'
                    or mpl.rcParams['text.usetex']):
                _try_distill(gs_distill,
                             tmppath, is_eps, ptype=papertype, bbox=bbox,
                             rotated=psfrag_rotated)
            elif mpl.rcParams['ps.usedistiller'] == 'xpdf':
                _try_distill(xpdf_distill,
                             tmppath, is_eps, ptype=papertype, bbox=bbox,
                             rotated=psfrag_rotated)

            _move_path_to_path_or_stream(tmppath, outfile)
