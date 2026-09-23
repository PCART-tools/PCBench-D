def wide_to_long(df, stubnames, i, j):
    """
    Wide panel to long format. Less flexible but more user-friendly than melt.

    Parameters
    ----------
    df : DataFrame
        The wide-format DataFrame
    stubnames : list
        A list of stub names. The wide format variables are assumed to
        start with the stub names.
    i : str
        The name of the id variable.
    j : str
        The name of the subobservation variable.
    stubend : str
        Regex to match for the end of the stubs.

    Returns
    -------
    DataFrame
        A DataFrame that contains each stub name as a variable as well as
        variables for i and j.

    Examples
    --------
    >>> import pandas as pd
    >>> import numpy as np
    >>> np.random.seed(123)
    >>> df = pd.DataFrame({"A1970" : {0 : "a", 1 : "b", 2 : "c"},
    ...                    "A1980" : {0 : "d", 1 : "e", 2 : "f"},
    ...                    "B1970" : {0 : 2.5, 1 : 1.2, 2 : .7},
    ...                    "B1980" : {0 : 3.2, 1 : 1.3, 2 : .1},
    ...                    "X"     : dict(zip(range(3), np.random.randn(3)))
    ...                   })
    >>> df["id"] = df.index
    >>> df
    A1970 A1980  B1970  B1980         X  id
    0     a     d    2.5    3.2 -1.085631   0
    1     b     e    1.2    1.3  0.997345   1
    2     c     f    0.7    0.1  0.282978   2
    >>> wide_to_long(df, ["A", "B"], i="id", j="year")
                    X  A    B
    id year
    0  1970 -1.085631  a  2.5
    1  1970  0.997345  b  1.2
    2  1970  0.282978  c  0.7
    0  1980 -1.085631  d  3.2
    1  1980  0.997345  e  1.3
    2  1980  0.282978  f  0.1

    Notes
    -----
    All extra variables are treated as extra id variables. This simply uses
    `pandas.melt` under the hood, but is hard-coded to "do the right thing"
    in a typicaly case.
    """

    def get_var_names(df, regex):
        return df.filter(regex=regex).columns.tolist()

    def melt_stub(df, stub, i, j):
        varnames = get_var_names(df, "^" + stub)
        newdf = melt(df, id_vars=i, value_vars=varnames, value_name=stub,
                     var_name=j)
        newdf_j = newdf[j].str.replace(stub, "")
        try:
            newdf_j = newdf_j.astype(int)
        except ValueError:
            pass
        newdf[j] = newdf_j
        return newdf

    id_vars = get_var_names(df, "^(?!%s)" % "|".join(stubnames))
    if i not in id_vars:
        id_vars += [i]

    newdf = melt_stub(df, stubnames[0], id_vars, j)

    for stub in stubnames[1:]:
        new = melt_stub(df, stub, id_vars, j)
        newdf = newdf.merge(new, how="outer", on=id_vars + [j], copy=False)
    return newdf.set_index([i, j])
