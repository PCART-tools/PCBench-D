@pytest.mark.parametrize('units', ['s', 'ms', 'us', 'ns'])
def test_date2num_NaT_scalar(units):
    tmpl = mdates.date2num(np.datetime64('NaT', units))
    assert np.isnan(tmpl)
