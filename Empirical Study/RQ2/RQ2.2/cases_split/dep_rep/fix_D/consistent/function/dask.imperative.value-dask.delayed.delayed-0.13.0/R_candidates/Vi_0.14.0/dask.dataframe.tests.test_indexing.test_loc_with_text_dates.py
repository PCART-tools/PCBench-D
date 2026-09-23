def test_loc_with_text_dates():
    A = tm.makeTimeSeries(10).iloc[:5]
    B = tm.makeTimeSeries(10).iloc[5:]
    s = dd.Series({('df', 0): A, ('df', 1): B}, 'df', A,
                  [A.index.min(), B.index.min(), B.index.max()])

    assert s.loc['2000': '2010'].divisions == s.divisions
    assert_eq(s.loc['2000': '2010'], s)
    assert len(s.loc['2000-01-03': '2000-01-05'].compute()) == 3
