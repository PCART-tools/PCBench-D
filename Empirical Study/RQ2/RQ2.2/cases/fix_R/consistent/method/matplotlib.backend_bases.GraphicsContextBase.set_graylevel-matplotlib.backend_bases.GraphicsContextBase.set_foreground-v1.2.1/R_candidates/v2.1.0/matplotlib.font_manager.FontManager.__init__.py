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

        verbose.report('font search path %s'%(str(paths)))
        #  Load TrueType fonts and create font dictionary.

        self.ttffiles = findSystemFonts(paths) + findSystemFonts()
        self.defaultFamily = {
            'ttf': 'DejaVu Sans',
            'afm': 'Helvetica'}
        self.defaultFont = {}

        for fname in self.ttffiles:
            verbose.report('trying fontname %s' % fname, 'debug')
            if fname.lower().find('DejaVuSans.ttf')>=0:
                self.defaultFont['ttf'] = fname
                break
        else:
            # use anything
            self.defaultFont['ttf'] = self.ttffiles[0]

        self.ttflist = createFontList(self.ttffiles)

        self.afmfiles = findSystemFonts(paths, fontext='afm') + \
            findSystemFonts(fontext='afm')
        self.afmlist = createFontList(self.afmfiles, fontext='afm')
        if len(self.afmfiles):
            self.defaultFont['afm'] = self.afmfiles[0]
        else:
            self.defaultFont['afm'] = None
