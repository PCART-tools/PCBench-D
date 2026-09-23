def test_meta_duplicated():
    df = pd.DataFrame(columns=['A', 'A', 'B'])
    res = meta_nonempty(df)

    exp = pd.DataFrame([['foo', 'foo', 'foo'],
                        ['foo', 'foo', 'foo']],
                       index=['a', 'b'],
                       columns=['A', 'A', 'B'])
    tm.assert_frame_equal(res, exp)
