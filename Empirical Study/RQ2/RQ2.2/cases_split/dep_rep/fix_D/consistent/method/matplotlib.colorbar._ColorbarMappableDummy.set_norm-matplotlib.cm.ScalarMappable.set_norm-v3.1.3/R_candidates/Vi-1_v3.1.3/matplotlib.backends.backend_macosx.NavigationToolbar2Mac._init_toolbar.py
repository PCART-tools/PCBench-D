    def _init_toolbar(self):
        basedir = os.path.join(rcParams['datapath'], "images")
        _macosx.NavigationToolbar2.__init__(self, basedir)
