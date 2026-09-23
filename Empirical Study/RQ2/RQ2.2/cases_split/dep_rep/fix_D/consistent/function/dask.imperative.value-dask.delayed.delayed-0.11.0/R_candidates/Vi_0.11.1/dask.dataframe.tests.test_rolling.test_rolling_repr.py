def test_rolling_repr():
    ddf = dd.from_pandas(pd.DataFrame([10] * 30), npartitions=3)
    assert repr(ddf.rolling(4)) in ['Rolling [window=4,center=False,axis=0]',
                                    'Rolling [window=4,axis=0,center=False]',
                                    'Rolling [center=False,axis=0,window=4]',
                                    'Rolling [center=False,window=4,axis=0]',
                                    'Rolling [axis=0,window=4,center=False]',
                                    'Rolling [axis=0,center=False,window=4]']
