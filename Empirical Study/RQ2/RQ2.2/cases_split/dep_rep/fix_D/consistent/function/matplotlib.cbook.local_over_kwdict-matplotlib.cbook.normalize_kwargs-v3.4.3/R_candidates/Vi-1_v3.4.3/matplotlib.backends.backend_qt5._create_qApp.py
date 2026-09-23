def _create_qApp():
    """
    Only one qApp can exist at a time, so check before creating one.
    """
    global qApp

    if qApp is None:
        app = QtWidgets.QApplication.instance()
        if app is None:
            # display_is_valid returns False only if on Linux and neither X11
            # nor Wayland display can be opened.
            if not mpl._c_internal_utils.display_is_valid():
                raise RuntimeError('Invalid DISPLAY variable')
            try:
                QtWidgets.QApplication.setAttribute(
                    QtCore.Qt.AA_EnableHighDpiScaling)
            except AttributeError:  # Attribute only exists for Qt>=5.6.
                pass
            try:
                QtWidgets.QApplication.setHighDpiScaleFactorRoundingPolicy(
                    QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
            except AttributeError:  # Added in Qt>=5.14.
                pass
            qApp = QtWidgets.QApplication(["matplotlib"])
            qApp.lastWindowClosed.connect(qApp.quit)
            cbook._setup_new_guiapp()
        else:
            qApp = app

    try:
        qApp.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)
    except AttributeError:
        pass
