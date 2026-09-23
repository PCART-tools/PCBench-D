    def __init__(self, size=None, weight='normal'):
        self._version = self.__version__

        self.__default_weight = weight
        self.default_size = size

        paths = [cbook._get_data_path('fonts', subdir)
                 for subdir in ['ttf', 'afm', 'pdfcorefonts']]
        #  Create list of font paths
        for pathname in ['TTFPATH', 'AFMPATH']:
            if pathname in os.environ:
                ttfpath = os.environ[pathname]
                if ttfpath.find(';') >= 0:  # win32 style
                    paths.extend(ttfpath.split(';'))
                elif ttfpath.find(':') >= 0:  # unix style
                    paths.extend(ttfpath.split(':'))
                else:
                    paths.append(ttfpath)
        _log.debug('font search path %s', str(paths))
        #  Load TrueType fonts and create font dictionary.

        self.defaultFamily = {
            'ttf': 'DejaVu Sans',
            'afm': 'Helvetica'}

        self.afmlist = []
        self.ttflist = []
        for fontext in ["afm", "ttf"]:
            for path in [*findSystemFonts(paths, fontext=fontext),
                         *findSystemFonts(fontext=fontext)]:
                try:
                    self.addfont(path)
                except OSError as exc:
                    _log.info("Failed to open font file %s: %s", path, exc)
                except Exception as exc:
                    _log.info("Failed to extract font properties from %s: %s",
                              path, exc)
