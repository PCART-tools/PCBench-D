def concat(dfs, axis=0, join='outer', uniform=False):
    """Concatenate, handling some edge cases:

    - Unions categoricals between partitions
    - Ignores empty partitions

    Parameters
    ----------
    dfs : list of DataFrame, Series, or Index
    axis : int or str, optional
    join : str, optional
    uniform : bool, optional
        Whether to treat ``dfs[0]`` as representative of ``dfs[1:]``. Set to
        True if all arguments have the same columns and dtypes (but not
        necessarily categories). Default is False.
    """
    if axis == 1:
        return pd.concat(dfs, axis=axis, join=join)

    # Support concatenating indices along axis 0
    if isinstance(dfs[0], pd.Index):
        if isinstance(dfs[0], pd.CategoricalIndex):
            return pd.CategoricalIndex(union_categoricals(dfs),
                                       name=dfs[0].name)
        return dfs[0].append(dfs[1:])

    # Handle categorical index separately
    if isinstance(dfs[0].index, pd.CategoricalIndex):
        dfs2 = [df.reset_index(drop=True) for df in dfs]
        ind = concat([df.index for df in dfs])
    else:
        dfs2 = dfs
        ind = None

    # Concatenate the partitions together, handling categories as needed
    if (isinstance(dfs2[0], pd.DataFrame) if uniform else
            any(isinstance(df, pd.DataFrame) for df in dfs2)):
        if uniform:
            dfs3 = dfs2
            cat_mask = dfs2[0].dtypes == 'category'
        else:
            # When concatenating mixed dataframes and series on axis 1, Pandas
            # converts series to dataframes with a single column named 0, then
            # concatenates.
            dfs3 = [df if isinstance(df, pd.DataFrame) else
                    df.rename(0).to_frame() for df in dfs2]
            cat_mask = pd.concat([(df.dtypes == 'category').to_frame().T
                                  for df in dfs3], join=join).any()

        if cat_mask.any():
            not_cat = cat_mask[~cat_mask].index
            out = pd.concat([df[df.columns.intersection(not_cat)]
                             for df in dfs3], join=join)
            for col in cat_mask.index.difference(not_cat):
                # Find an example of categoricals in this column
                for df in dfs3:
                    sample = df.get(col)
                    if sample is not None:
                        break
                # Extract partitions, subbing in missing if needed
                parts = []
                for df in dfs3:
                    if col in df.columns:
                        parts.append(df[col])
                    else:
                        codes = np.full(len(df), -1, dtype='i8')
                        data = pd.Categorical.from_codes(codes,
                                                         sample.cat.categories,
                                                         sample.cat.ordered)
                        parts.append(data)
                out[col] = union_categoricals(parts)
            out = out.reindex_axis(cat_mask.index, axis=1)
        else:
            out = pd.concat(dfs3, join=join)
    else:
        if is_categorical_dtype(dfs2[0].dtype):
            if ind is None:
                ind = concat([df.index for df in dfs2])
            return pd.Series(union_categoricals(dfs2), index=ind,
                             name=dfs2[0].name)
        out = pd.concat(dfs2, join=join)
    # Re-add the index if needed
    if ind is not None:
        out.index = ind
    return out
