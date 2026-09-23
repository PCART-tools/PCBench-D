    def __init__(self, lines):
        import gtk.glade

        datadir = matplotlib.get_data_path()
        gladefile = os.path.join(datadir, 'lineprops.glade')
        if not os.path.exists(gladefile):
            raise IOError(
                'Could not find gladefile lineprops.glade in %s' % datadir)

        self._inited = False
        self._updateson = True # suppress updates when setting widgets manually
        self.wtree = gtk.glade.XML(gladefile, 'dialog_lineprops')
        self.wtree.signal_autoconnect(
            {s: getattr(self, s) for s in self.signals})

        self.dlg = self.wtree.get_widget('dialog_lineprops')

        self.lines = lines

        cbox = self.wtree.get_widget('combobox_lineprops')
        cbox.set_active(0)
        self.cbox_lineprops = cbox

        cbox = self.wtree.get_widget('combobox_linestyles')
        for ls in self.linestyles:
            cbox.append_text(ls)
        cbox.set_active(0)
        self.cbox_linestyles = cbox

        cbox = self.wtree.get_widget('combobox_markers')
        for m in self.markers:
            cbox.append_text(m)
        cbox.set_active(0)
        self.cbox_markers = cbox
        self._lastcnt = 0
        self._inited = True
