@pytest.mark.parametrize(
    "qt_key, qt_mods, answer",
    [
        ("Key_A", ["ShiftModifier"], "A"),
        ("Key_A", [], "a"),
        ("Key_A", ["ControlModifier"], ("ctrl+a")),
        (
            "Key_Aacute",
            ["ShiftModifier"],
            "\N{LATIN CAPITAL LETTER A WITH ACUTE}",
        ),
        ("Key_Aacute", [], "\N{LATIN SMALL LETTER A WITH ACUTE}"),
        ("Key_Control", ["AltModifier"], ("alt+control")),
        ("Key_Alt", ["ControlModifier"], "ctrl+alt"),
        (
            "Key_Aacute",
            ["ControlModifier", "AltModifier", "MetaModifier"],
            ("ctrl+alt+meta+\N{LATIN SMALL LETTER A WITH ACUTE}"),
        ),
        # We do not currently map the media keys, this may change in the
        # future.  This means the callback will never fire
        ("Key_Play", [], None),
        ("Key_Backspace", [], "backspace"),
        (
            "Key_Backspace",
            ["ControlModifier"],
            "ctrl+backspace",
        ),
    ],
    ids=[
        'shift',
        'lower',
        'control',
        'unicode_upper',
        'unicode_lower',
        'alt_control',
        'control_alt',
        'modifier_order',
        'non_unicode_key',
        'backspace',
        'backspace_mod',
    ]
)
@pytest.mark.parametrize('backend', [
    # Note: the value is irrelevant; the important part is the marker.
    pytest.param(
        'Qt5Agg',
        marks=pytest.mark.backend('Qt5Agg', skip_on_importerror=True)),
    pytest.param(
        'QtAgg',
        marks=pytest.mark.backend('QtAgg', skip_on_importerror=True)),
])
def test_correct_key(backend, qt_core, qt_key, qt_mods, answer):
    """
    Make a figure.
    Send a key_press_event event (using non-public, qtX backend specific api).
    Catch the event.
    Assert sent and caught keys are the same.
    """
    from matplotlib.backends.qt_compat import _enum, _to_int

    if sys.platform == "darwin" and answer is not None:
        answer = answer.replace("ctrl", "cmd")
        answer = answer.replace("control", "cmd")
        answer = answer.replace("meta", "ctrl")
    result = None
    qt_mod = _enum("QtCore.Qt.KeyboardModifier").NoModifier
    for mod in qt_mods:
        qt_mod |= getattr(_enum("QtCore.Qt.KeyboardModifier"), mod)

    class _Event:
        def isAutoRepeat(self): return False
        def key(self): return _to_int(getattr(_enum("QtCore.Qt.Key"), qt_key))
        def modifiers(self): return qt_mod

    def on_key_press(event):
        nonlocal result
        result = event.key

    qt_canvas = plt.figure().canvas
    qt_canvas.mpl_connect('key_press_event', on_key_press)
    qt_canvas.keyPressEvent(_Event())
    assert result == answer
