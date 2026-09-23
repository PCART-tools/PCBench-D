def test_subs_with_surprisingly_friendly_eq():
    try:
        import pandas as pd
    except:
        return
    else:
        df = pd.DataFrame()
        assert subs(df, 'x', 1) is df
