    def __init__(self, size=None, weight='normal'):
        self._version = self.__version__

        self.__default_weight = weight
        self.default_size = size

        paths = [os.path.join(rcParams['datapath'], 'fonts', 'ttf'),
                 os.path.join(rcParams['datapath'], 'fonts', 'afm'),
                 os.path.join(rcParams['datapath'], 'fonts', 'pdfcorefonts')]

        #  Create list of font paths
        for pathname in ['TTFPATH', 'AFMPATH']:
            if pathname in os.environ:
                ttfpath = os.environ[pathname]
                if ttfpath.find(';') >= 0: #win32 style
                    paths.extend(ttfpath.split(';'))
                elif ttfpath.find(':') >= 0: # unix style
                    paths.extend(ttfpath.split(':'))
                else:
                    paths.append(ttfpath)
        _log.debug('font search path %s', str(paths))
        #  Load TrueType fonts and create font dictionary.

        self.defaultFamily = {
            'ttf': 'DejaVu Sans',
            'afm': 'Helvetica'}
        self.defaultFont = {}

        ttffiles = findSystemFonts(paths) + findSystemFonts()
        self.defaultFont['ttf'] = next(
            (fname for fname in ttffiles
             if fname.lower().endswith("dejavusans.ttf")),
            ttffiles[0])
        self.ttflist = createFontList(ttffiles)

        afmfiles = (findSystemFonts(paths, fontext='afm')
                    + findSystemFonts(fontext='afm'))
        self.afmlist = createFontList(afmfiles, fontext='afm')
        self.defaultFont['afm'] = afmfiles[0] if afmfiles else None
