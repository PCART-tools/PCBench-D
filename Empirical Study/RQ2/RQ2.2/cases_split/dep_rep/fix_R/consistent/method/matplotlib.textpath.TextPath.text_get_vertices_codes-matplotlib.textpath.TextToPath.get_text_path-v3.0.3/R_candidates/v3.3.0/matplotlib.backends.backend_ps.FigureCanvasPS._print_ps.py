    def _print_ps(
            self, outfile, format, *args,
            dpi=72, metadata=None, papertype=None, orientation='portrait',
            **kwargs):

        self.figure.set_dpi(72)  # Override the dpi kwarg

        dsc_comments = {}
        if isinstance(outfile, (str, os.PathLike)):
            dsc_comments["Title"] = \
                os.fspath(outfile).encode("ascii", "replace").decode("ascii")
        dsc_comments["Creator"] = (metadata or {}).get(
            "Creator",
            f"matplotlib version {mpl.__version__}, http://matplotlib.org/")
        # See https://reproducible-builds.org/specs/source-date-epoch/
        source_date_epoch = os.getenv("SOURCE_DATE_EPOCH")
        dsc_comments["CreationDate"] = (
            datetime.datetime.utcfromtimestamp(
                int(source_date_epoch)).strftime("%a %b %d %H:%M:%S %Y")
            if source_date_epoch
            else time.ctime())
        dsc_comments = "\n".join(
            f"%%{k}: {v}" for k, v in dsc_comments.items())

        if papertype is None:
            papertype = mpl.rcParams['ps.papersize']
        papertype = papertype.lower()
        cbook._check_in_list(['auto', *papersize], papertype=papertype)

        orientation = cbook._check_getitem(
            _Orientation, orientation=orientation.lower())

        printer = (self._print_figure_tex
                   if mpl.rcParams['text.usetex'] else
                   self._print_figure)
        printer(outfile, format, dpi=dpi, dsc_comments=dsc_comments,
                orientation=orientation, papertype=papertype, **kwargs)
