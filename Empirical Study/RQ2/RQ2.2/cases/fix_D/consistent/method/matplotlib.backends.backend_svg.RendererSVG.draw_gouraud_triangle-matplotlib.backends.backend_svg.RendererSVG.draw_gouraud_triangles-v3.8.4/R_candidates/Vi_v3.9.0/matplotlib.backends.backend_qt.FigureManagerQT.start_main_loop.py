    @classmethod
    def start_main_loop(cls):
        qapp = QtWidgets.QApplication.instance()
        if qapp:
            with _allow_interrupt_qt(qapp):
                qt_compat._exec(qapp)
