@pytest.mark.parametrize('npartitions', [1, 2, 3])
@pytest.mark.parametrize('method,args,check_less_precise', [
    ('count', (), False),
    ('sum', (), False),
    ('mean', (), False),
    ('median', (), False),
    ('min', (), False),
    ('max', (), False),
    ('std', (), False),
    ('var', (), False),
    ('skew', (), True), # here and elsewhere, results for kurt and skew are
    ('kurt', (), True), # checked with check_less_precise=True so that we are
                        # only looking at 3ish decimal places for the equality check
                        # rather than 5ish. I have encountered a case where a test
                        # seems to have failed due to numerical problems with kurt.
                        # So far, I am only weakening the check for kurt and skew,
                        # as they involve third degree powers and higher
    ('quantile', (.38,), False),
    ('apply', (np.sum,), False),
])
@pytest.mark.parametrize('window', [1, 2, 4, 5])
@pytest.mark.parametrize('center', [True, False])
@pytest.mark.parametrize('axis', [0, 'columns'])
def test_rolling_dataframe(npartitions, method, args, window, center, axis,
                           check_less_precise):
    if method == 'count' and axis in [1, 'columns']:
        pytest.xfail('count currently ignores the axis argument.')

    N = 40
    df = pd.DataFrame({'a': np.random.randn(N).cumsum(),
                       'b': np.random.randint(100, size=(N,)),
                       'c': np.random.randint(100, size=(N,)),
                       'd': np.random.randint(100, size=(N,)),
                       'e': np.random.randint(100, size=(N,))})
    ddf = dd.from_pandas(df, npartitions)

    prolling = df.rolling(window, center=center, axis=axis)
    drolling = ddf.rolling(window, center=center, axis=axis)
    eq(getattr(prolling, method)(*args), getattr(drolling, method)(*args),
       check_less_precise=check_less_precise)
