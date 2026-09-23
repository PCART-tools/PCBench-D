@_Backend.export
class _BackendQT(_Backend):
    FigureCanvas = FigureCanvasQT
    FigureManager = FigureManagerQT

    @staticmethod
    def mainloop():
        with _maybe_allow_interrupt(qApp):
            qt_compat._exec(qApp)
