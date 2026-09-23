@pytest.mark.parametrize(
    'qt_key, qt_mods, answer',
    [
        ('Key_A', ['ShiftModifier'], 'A'),
        ('Key_A', [], 'a'),
        ('Key_A', ['ControlModifier'], 'ctrl+a'),
        ('Key_Aacute', ['ShiftModifier'],
         '\N{LATIN CAPITAL LETTER A WITH ACUTE}'),
        ('Key_Aacute', [],
         '\N{LATIN SMALL LETTER A WITH ACUTE}'),
        ('Key_Control', ['AltModifier'], 'alt+control'),
        ('Key_Alt', ['ControlModifier'], 'ctrl+alt'),
        ('Key_Aacute', ['ControlModifier', 'AltModifier', 'MetaModifier'],
         'ctrl+alt+super+\N{LATIN SMALL LETTER A WITH ACUTE}'),
        ('Key_Play', [], None),
        ('Key_Backspace', [], 'backspace'),
        ('Key_Backspace', ['ControlModifier'], 'ctrl+backspace'),
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
        'Qt4Agg',
        marks=pytest.mark.backend('Qt4Agg', skip_on_importerror=True)),
    pytest.param(
        'Qt5Agg',
        marks=pytest.mark.backend('Qt5Agg', skip_on_importerror=True)),
])
def test_correct_key(backend, qt_core, qt_key, qt_mods, answer):
    """
    Make a figure.
    Send a key_press_event event (using non-public, qtX backend specific api).
    Catch the event.
    Assert sent and caught keys are the same.
    """
    qt_mod = qt_core.Qt.NoModifier
    for mod in qt_mods:
        qt_mod |= getattr(qt_core.Qt, mod)

    class _Event:
        def isAutoRepeat(self): return False
        def key(self): return getattr(qt_core.Qt, qt_key)
        def modifiers(self): return qt_mod

    def on_key_press(event):
        assert event.key == answer

    qt_canvas = plt.figure().canvas
    qt_canvas.mpl_connect('key_press_event', on_key_press)
    qt_canvas.keyPressEvent(_Event())
