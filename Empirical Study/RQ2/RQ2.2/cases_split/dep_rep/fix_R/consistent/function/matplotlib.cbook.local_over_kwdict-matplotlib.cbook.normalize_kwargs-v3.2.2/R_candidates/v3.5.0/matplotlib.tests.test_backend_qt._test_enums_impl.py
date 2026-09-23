def _test_enums_impl():
    import sys

    from matplotlib.backends.qt_compat import _enum, _to_int, QtCore
    from matplotlib.backend_bases import cursors, MouseButton

    _enum("QtGui.QDoubleValidator.State").Acceptable

    _enum("QtWidgets.QDialogButtonBox.StandardButton").Ok
    _enum("QtWidgets.QDialogButtonBox.StandardButton").Cancel
    _enum("QtWidgets.QDialogButtonBox.StandardButton").Apply
    for btn_type in ["Ok", "Cancel"]:
        getattr(_enum("QtWidgets.QDialogButtonBox.StandardButton"), btn_type)

    _enum("QtGui.QImage.Format").Format_ARGB32_Premultiplied
    _enum("QtGui.QImage.Format").Format_ARGB32_Premultiplied
    # SPECIAL_KEYS are Qt::Key that do *not* return their unicode name instead
    # they have manually specified names.
    SPECIAL_KEYS = {
        _to_int(getattr(_enum("QtCore.Qt.Key"), k)): v
        for k, v in [
            ("Key_Escape", "escape"),
            ("Key_Tab", "tab"),
            ("Key_Backspace", "backspace"),
            ("Key_Return", "enter"),
            ("Key_Enter", "enter"),
            ("Key_Insert", "insert"),
            ("Key_Delete", "delete"),
            ("Key_Pause", "pause"),
            ("Key_SysReq", "sysreq"),
            ("Key_Clear", "clear"),
            ("Key_Home", "home"),
            ("Key_End", "end"),
            ("Key_Left", "left"),
            ("Key_Up", "up"),
            ("Key_Right", "right"),
            ("Key_Down", "down"),
            ("Key_PageUp", "pageup"),
            ("Key_PageDown", "pagedown"),
            ("Key_Shift", "shift"),
            # In OSX, the control and super (aka cmd/apple) keys are switched.
            ("Key_Control", "control" if sys.platform != "darwin" else "cmd"),
            ("Key_Meta", "meta" if sys.platform != "darwin" else "control"),
            ("Key_Alt", "alt"),
            ("Key_CapsLock", "caps_lock"),
            ("Key_F1", "f1"),
            ("Key_F2", "f2"),
            ("Key_F3", "f3"),
            ("Key_F4", "f4"),
            ("Key_F5", "f5"),
            ("Key_F6", "f6"),
            ("Key_F7", "f7"),
            ("Key_F8", "f8"),
            ("Key_F9", "f9"),
            ("Key_F10", "f10"),
            ("Key_F10", "f11"),
            ("Key_F12", "f12"),
            ("Key_Super_L", "super"),
            ("Key_Super_R", "super"),
        ]
    }
    # Define which modifier keys are collected on keyboard events.  Elements
    # are (Qt::KeyboardModifiers, Qt::Key) tuples.  Order determines the
    # modifier order (ctrl+alt+...) reported by Matplotlib.
    _MODIFIER_KEYS = [
        (
            _to_int(getattr(_enum("QtCore.Qt.KeyboardModifier"), mod)),
            _to_int(getattr(_enum("QtCore.Qt.Key"), key)),
        )
        for mod, key in [
            ("ControlModifier", "Key_Control"),
            ("AltModifier", "Key_Alt"),
            ("ShiftModifier", "Key_Shift"),
            ("MetaModifier", "Key_Meta"),
        ]
    ]
    cursord = {
        k: getattr(_enum("QtCore.Qt.CursorShape"), v)
        for k, v in [
            (cursors.MOVE, "SizeAllCursor"),
            (cursors.HAND, "PointingHandCursor"),
            (cursors.POINTER, "ArrowCursor"),
            (cursors.SELECT_REGION, "CrossCursor"),
            (cursors.WAIT, "WaitCursor"),
        ]
    }

    buttond = {
        getattr(_enum("QtCore.Qt.MouseButton"), k): v
        for k, v in [
            ("LeftButton", MouseButton.LEFT),
            ("RightButton", MouseButton.RIGHT),
            ("MiddleButton", MouseButton.MIDDLE),
            ("XButton1", MouseButton.BACK),
            ("XButton2", MouseButton.FORWARD),
        ]
    }

    _enum("QtCore.Qt.WidgetAttribute").WA_OpaquePaintEvent
    _enum("QtCore.Qt.FocusPolicy").StrongFocus
    _enum("QtCore.Qt.ToolBarArea").TopToolBarArea
    _enum("QtCore.Qt.ToolBarArea").TopToolBarArea
    _enum("QtCore.Qt.AlignmentFlag").AlignRight
    _enum("QtCore.Qt.AlignmentFlag").AlignVCenter
    _enum("QtWidgets.QSizePolicy.Policy").Expanding
    _enum("QtWidgets.QSizePolicy.Policy").Ignored
    _enum("QtCore.Qt.MaskMode").MaskOutColor
    _enum("QtCore.Qt.ToolBarArea").TopToolBarArea
    _enum("QtCore.Qt.ToolBarArea").TopToolBarArea
    _enum("QtCore.Qt.AlignmentFlag").AlignRight
    _enum("QtCore.Qt.AlignmentFlag").AlignVCenter
    _enum("QtWidgets.QSizePolicy.Policy").Expanding
    _enum("QtWidgets.QSizePolicy.Policy").Ignored
