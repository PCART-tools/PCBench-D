@_Backend.export
class _BackendQT5(_Backend):
    required_interactive_framework = "qt5"
    FigureCanvas = FigureCanvasQT
    FigureManager = FigureManagerQT

    @staticmethod
    def trigger_manager_draw(manager):
        manager.canvas.draw_idle()

    @staticmethod
    def mainloop():
        # allow KeyboardInterrupt exceptions to close the plot window.
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        qApp.exec_()
