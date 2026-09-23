@_Backend.export
class _BackendGTK3(_Backend):
    required_interactive_framework = "gtk3"
    FigureCanvas = FigureCanvasGTK3
    FigureManager = FigureManagerGTK3

    @staticmethod
    def trigger_manager_draw(manager):
        manager.canvas.draw_idle()

    @staticmethod
    def mainloop():
        if Gtk.main_level() == 0:
            Gtk.main()
