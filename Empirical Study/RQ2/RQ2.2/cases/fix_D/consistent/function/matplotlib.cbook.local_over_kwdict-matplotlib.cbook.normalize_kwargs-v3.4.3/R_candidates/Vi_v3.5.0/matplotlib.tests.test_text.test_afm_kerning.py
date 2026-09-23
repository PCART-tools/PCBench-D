def test_afm_kerning():
    fn = mpl.font_manager.findfont("Helvetica", fontext="afm")
    with open(fn, 'rb') as fh:
        afm = mpl.afm.AFM(fh)
    assert afm.string_width_height('VAVAVAVAVAVA') == (7174.0, 718)
