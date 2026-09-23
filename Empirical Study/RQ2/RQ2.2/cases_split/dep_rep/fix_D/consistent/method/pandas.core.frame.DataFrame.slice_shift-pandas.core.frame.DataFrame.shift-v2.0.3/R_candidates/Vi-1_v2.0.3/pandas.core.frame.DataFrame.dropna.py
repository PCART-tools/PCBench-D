    def dropna(
        self,
        *,
        axis: Axis = 0,
        how: AnyAll | NoDefault = no_default,
        thresh: int | NoDefault = no_default,
        subset: IndexLabel = None,
        inplace: bool = False,
        ignore_index: bool = False,
    ) -> DataFrame | None:
        """
        Remove missing values.

        See the :ref:`User Guide <missing_data>` for more on which values are
        considered missing, and how to work with missing data.

        Parameters
        ----------
        axis : {0 or 'index', 1 or 'columns'}, default 0
            Determine if rows or columns which contain missing values are
            removed.

            * 0, or 'index' : Drop rows which contain missing values.
            * 1, or 'columns' : Drop columns which contain missing value.

            Pass tuple or list to drop on multiple axes.
            Only a single axis is allowed.

        how : {'any', 'all'}, default 'any'
            Determine if row or column is removed from DataFrame, when we have
            at least one NA or all NA.

            * 'any' : If any NA values are present, drop that row or column.
            * 'all' : If all values are NA, drop that row or column.

        thresh : int, optional
            Require that many non-NA values. Cannot be combined with how.
        subset : column label or sequence of labels, optional
            Labels along other axis to consider, e.g. if you are dropping rows
            these would be a list of columns to include.
        inplace : bool, default False
            Whether to modify the DataFrame rather than creating a new one.
        ignore_index : bool, default ``False``
            If ``True``, the resulting axis will be labeled 0, 1, …, n - 1.

            .. versionadded:: 2.0.0

        Returns
        -------
        DataFrame or None
            DataFrame with NA entries dropped from it or None if ``inplace=True``.

        See Also
        --------
        DataFrame.isna: Indicate missing values.
        DataFrame.notna : Indicate existing (non-missing) values.
        DataFrame.fillna : Replace missing values.
        Series.dropna : Drop missing values.
        Index.dropna : Drop missing indices.

        Examples
        --------
        >>> df = pd.DataFrame({"name": ['Alfred', 'Batman', 'Catwoman'],
        ...                    "toy": [np.nan, 'Batmobile', 'Bullwhip'],
        ...                    "born": [pd.NaT, pd.Timestamp("1940-04-25"),
        ...                             pd.NaT]})
        >>> df
               name        toy       born
        0    Alfred        NaN        NaT
        1    Batman  Batmobile 1940-04-25
        2  Catwoman   Bullwhip        NaT

        Drop the rows where at least one element is missing.

        >>> df.dropna()
             name        toy       born
        1  Batman  Batmobile 1940-04-25

        Drop the columns where at least one element is missing.

        >>> df.dropna(axis='columns')
               name
        0    Alfred
        1    Batman
        2  Catwoman

        Drop the rows where all elements are missing.

        >>> df.dropna(how='all')
               name        toy       born
        0    Alfred        NaN        NaT
        1    Batman  Batmobile 1940-04-25
        2  Catwoman   Bullwhip        NaT

        Keep only the rows with at least 2 non-NA values.

        >>> df.dropna(thresh=2)
               name        toy       born
        1    Batman  Batmobile 1940-04-25
        2  Catwoman   Bullwhip        NaT

        Define in which columns to look for missing values.

        >>> df.dropna(subset=['name', 'toy'])
               name        toy       born
        1    Batman  Batmobile 1940-04-25
        2  Catwoman   Bullwhip        NaT
        """
        if (how is not no_default) and (thresh is not no_default):
            raise TypeError(
                "You cannot set both the how and thresh arguments at the same time."
            )

        if how is no_default:
            how = "any"

        inplace = validate_bool_kwarg(inplace, "inplace")
        if isinstance(axis, (tuple, list)):
            # GH20987
            raise TypeError("supplying multiple axes to axis is no longer supported.")

        axis = self._get_axis_number(axis)
        agg_axis = 1 - axis

        agg_obj = self
        if subset is not None:
            # subset needs to be list
            if not is_list_like(subset):
                subset = [subset]
            ax = self._get_axis(agg_axis)
            indices = ax.get_indexer_for(subset)
            check = indices == -1
            if check.any():
                raise KeyError(np.array(subset)[check].tolist())
            agg_obj = self.take(indices, axis=agg_axis)

        if thresh is not no_default:
            count = agg_obj.count(axis=agg_axis)
            mask = count >= thresh
        elif how == "any":
            # faster equivalent to 'agg_obj.count(agg_axis) == self.shape[agg_axis]'
            mask = notna(agg_obj).all(axis=agg_axis, bool_only=False)
        elif how == "all":
            # faster equivalent to 'agg_obj.count(agg_axis) > 0'
            mask = notna(agg_obj).any(axis=agg_axis, bool_only=False)
        else:
            raise ValueError(f"invalid how option: {how}")

        if np.all(mask):
            result = self.copy(deep=None)
        else:
            result = self.loc(axis=axis)[mask]

        if ignore_index:
            result.index = default_index(len(result))

        if not inplace:
            return result
        self._update_inplace(result)
        return None
