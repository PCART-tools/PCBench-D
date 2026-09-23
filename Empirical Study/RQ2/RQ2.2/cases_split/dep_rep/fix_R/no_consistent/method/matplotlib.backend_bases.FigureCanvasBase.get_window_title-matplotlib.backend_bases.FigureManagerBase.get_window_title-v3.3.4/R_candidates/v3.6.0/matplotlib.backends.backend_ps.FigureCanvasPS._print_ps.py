    @_api.delete_parameter("3.5", "args")
    def _print_ps(
            self, fmt, outfile, *args,
            metadata=None, papertype=None, orientation='portrait',
            **kwargs):

        dpi = self.figure.dpi
        self.figure.dpi = 72  # Override the dpi kwarg

        dsc_comments = {}
        if isinstance(outfile, (str, os.PathLike)):
            filename = pathlib.Path(outfile).name
            dsc_comments["Title"] = \
                filename.encode("ascii", "replace").decode("ascii")
        dsc_comments["Creator"] = (metadata or {}).get(
            "Creator",
            f"Matplotlib v{mpl.__version__}, https://matplotlib.org/")
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
        _api.check_in_list(['auto', *papersize], papertype=papertype)

        orientation = _api.check_getitem(
            _Orientation, orientation=orientation.lower())

        printer = (self._print_figure_tex
                   if mpl.rcParams['text.usetex'] else
                   self._print_figure)
        printer(fmt, outfile, dpi=dpi, dsc_comments=dsc_comments,
                orientation=orientation, papertype=papertype, **kwargs)
