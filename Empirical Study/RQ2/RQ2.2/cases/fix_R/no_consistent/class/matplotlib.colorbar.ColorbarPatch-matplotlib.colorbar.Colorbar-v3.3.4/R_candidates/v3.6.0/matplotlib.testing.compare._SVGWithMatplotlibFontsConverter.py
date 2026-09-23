class _SVGWithMatplotlibFontsConverter(_SVGConverter):
    """
    A SVG converter which explicitly adds the fonts shipped by Matplotlib to
    Inkspace's font search path, to better support `svg.fonttype = "none"`
    (which is in particular used by certain mathtext tests).
    """

    def __call__(self, orig, dest):
        if not hasattr(self, "_tmpdir"):
            self._tmpdir = TemporaryDirectory()
            shutil.copytree(cbook._get_data_path("fonts/ttf"),
                            Path(self._tmpdir.name, "fonts"))
        return super().__call__(orig, dest)
