@pytest.mark.parametrize('equiv_styles',
                         [('mpl20', 'default'),
                          ('mpl15', 'classic')],
                         ids=['mpl20', 'mpl15'])
def test_alias(equiv_styles):
    rc_dicts = []
    for sty in equiv_styles:
        with style.context(sty):
            rc_dicts.append(mpl.rcParams.copy())

    rc_base = rc_dicts[0]
    for nm, rc in zip(equiv_styles[1:], rc_dicts[1:]):
        assert rc_base == rc
