@pytest.mark.parametrize('data',
    [pd.Series([1, 1, 1, 2, 2, 1, 3, 4], dtype='category'),
     pd.Series(pd.Categorical([1, 1, 1, 2, 2, 1, 3, 4], categories=[4, 3, 2, 1])),
     pd.DataFrame({'a': [1, 2, 3, 4, 4, 3, 2, 1],
                   'b': pd.Categorical(list('abcdabcd'))}),
    ]
)
def test_get_dummies(data):
    exp = pd.get_dummies(data)

    ddata = dd.from_pandas(data, 2)
    res = dd.get_dummies(ddata)
    assert eq(res, exp)
    tm.assert_index_equal(res.columns, exp.columns)
