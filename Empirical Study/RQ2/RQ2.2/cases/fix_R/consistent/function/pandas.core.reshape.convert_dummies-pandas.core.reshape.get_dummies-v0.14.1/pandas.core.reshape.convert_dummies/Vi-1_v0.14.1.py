def convert_dummies(data, cat_variables, prefix_sep='_'):
    """
    Compute DataFrame with specified columns converted to dummy variables (0 /
    1). Result columns will be prefixed with the column name, then the level
    name, e.g. 'A_foo' for column A and level foo

    Parameters
    ----------
    data : DataFrame
    cat_variables : list-like
        Must be column names in the DataFrame
    prefix_sep : string, default '_'
        String to use to separate column name from dummy level

    Returns
    -------
    dummies : DataFrame
    """
    result = data.drop(cat_variables, axis=1)
    for variable in cat_variables:
        dummies = get_dummies(data[variable], prefix=variable,
                              prefix_sep=prefix_sep)
        result = result.join(dummies)
    return result
