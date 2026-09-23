def groupby_error():
    pdf = pd.DataFrame({'x': [1, 2, 3, 4, 6, 7, 8, 9, 10],
                        'y': list('abcbabbcda')})
    ddf = dd.from_pandas(pdf, 3)

    with tm.assertRaises(KeyError):
        ddf.groupby('A')

    with tm.assertRaises(KeyError):
        ddf.groupby(['x', 'A'])

    dp = ddf.groupby('y')

    msg = 'Column not found: '
    with tm.assertRaisesRegexp(KeyError, msg):
        dp['A']

    with tm.assertRaisesRegexp(KeyError, msg):
        dp[['x', 'A']]
