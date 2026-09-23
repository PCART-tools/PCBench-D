@_Backend.export
class _BackendQT(_Backend):
    FigureCanvas = FigureCanvasQT
    FigureManager = FigureManagerQT

    @staticmethod
    def mainloop():
        qapp = QtWidgets.QApplication.instance()
        with _maybe_allow_interrupt(qapp):
            qt_compat._exec(qapp)
