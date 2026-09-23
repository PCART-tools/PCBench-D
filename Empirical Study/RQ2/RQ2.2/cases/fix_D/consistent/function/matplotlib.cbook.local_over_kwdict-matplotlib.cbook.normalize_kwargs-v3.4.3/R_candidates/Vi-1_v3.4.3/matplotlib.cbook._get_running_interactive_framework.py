def _get_running_interactive_framework():
    """
    Return the interactive framework whose event loop is currently running, if
    any, or "headless" if no event loop can be started, or None.

    Returns
    -------
    Optional[str]
        One of the following values: "qt5", "qt4", "gtk3", "wx", "tk",
        "macosx", "headless", ``None``.
    """
    QtWidgets = (sys.modules.get("PyQt5.QtWidgets")
                 or sys.modules.get("PySide2.QtWidgets"))
    if QtWidgets and QtWidgets.QApplication.instance():
        return "qt5"
    QtGui = (sys.modules.get("PyQt4.QtGui")
             or sys.modules.get("PySide.QtGui"))
    if QtGui and QtGui.QApplication.instance():
        return "qt4"
    Gtk = sys.modules.get("gi.repository.Gtk")
    if Gtk and Gtk.main_level():
        return "gtk3"
    wx = sys.modules.get("wx")
    if wx and wx.GetApp():
        return "wx"
    tkinter = sys.modules.get("tkinter")
    if tkinter:
        codes = {tkinter.mainloop.__code__, tkinter.Misc.mainloop.__code__}
        for frame in sys._current_frames().values():
            while frame:
                if frame.f_code in codes:
                    return "tk"
                frame = frame.f_back
    if 'matplotlib.backends._macosx' in sys.modules:
        if sys.modules["matplotlib.backends._macosx"].event_loop_is_running():
            return "macosx"
    if not _c_internal_utils.display_is_valid():
        return "headless"
    return None
