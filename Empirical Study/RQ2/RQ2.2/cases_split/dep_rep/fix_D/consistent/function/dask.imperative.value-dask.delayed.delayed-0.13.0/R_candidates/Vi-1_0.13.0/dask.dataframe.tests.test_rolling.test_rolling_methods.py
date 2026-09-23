@pytest.mark.parametrize('method,args,check_less_precise', [
    ('count', (), False),
    ('sum', (), False),
    ('mean', (), False),
    ('median', (), False),
    ('min', (), False),
    ('max', (), False),
    ('std', (), False),
    ('var', (), False),
    ('skew', (), True),   # here and elsewhere, results for kurt and skew are
    ('kurt', (), True),   # checked with check_less_precise=True so that we are
                          # only looking at 3ish decimal places for the equality check
                          # rather than 5ish. I have encountered a case where a test
                          # seems to have failed due to numerical problems with kurt.
                          # So far, I am only weakening the check for kurt and skew,
                          # as they involve third degree powers and higher
    ('quantile', (.38,), False),
    ('apply', (mad,), False),
])
@pytest.mark.parametrize('window', [1, 2, 4, 5])
@pytest.mark.parametrize('center', [True, False])
def test_rolling_methods(method, args, window, center, check_less_precise):
    # DataFrame
    prolling = df.rolling(window, center=center)
    drolling = ddf.rolling(window, center=center)
    assert_eq(getattr(prolling, method)(*args),
              getattr(drolling, method)(*args),
              check_less_precise=check_less_precise)

    # Series
    prolling = df.a.rolling(window, center=center)
    drolling = ddf.a.rolling(window, center=center)
    assert_eq(getattr(prolling, method)(*args),
              getattr(drolling, method)(*args),
              check_less_precise=check_less_precise)
