    def __init__(self, renderer):
        GraphicsContextBase.__init__(self)
        self.renderer = renderer
        self.gdkGC    = gtk.gdk.GC(renderer.gdkDrawable)
        self._cmap    = renderer._cmap
