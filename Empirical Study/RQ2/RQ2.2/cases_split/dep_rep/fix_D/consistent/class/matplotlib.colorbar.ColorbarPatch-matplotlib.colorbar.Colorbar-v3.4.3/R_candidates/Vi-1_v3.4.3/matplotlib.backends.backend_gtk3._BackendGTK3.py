@_Backend.export
class _BackendGTK3(_Backend):
    FigureCanvas = FigureCanvasGTK3
    FigureManager = FigureManagerGTK3

    @staticmethod
    def mainloop():
        if Gtk.main_level() == 0:
            cbook._setup_new_guiapp()
            Gtk.main()
