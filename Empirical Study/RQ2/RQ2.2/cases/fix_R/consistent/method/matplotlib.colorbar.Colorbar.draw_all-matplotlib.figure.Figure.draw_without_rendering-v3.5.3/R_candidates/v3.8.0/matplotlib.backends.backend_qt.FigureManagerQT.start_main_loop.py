    @classmethod
    def start_main_loop(cls):
        qapp = QtWidgets.QApplication.instance()
        if qapp:
            with _maybe_allow_interrupt(qapp):
                qt_compat._exec(qapp)
