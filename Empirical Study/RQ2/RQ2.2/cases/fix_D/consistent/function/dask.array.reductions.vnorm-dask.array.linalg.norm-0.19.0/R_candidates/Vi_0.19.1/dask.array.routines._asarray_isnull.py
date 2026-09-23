def _asarray_isnull(values):
    import pandas as pd
    return np.asarray(pd.isnull(values))
