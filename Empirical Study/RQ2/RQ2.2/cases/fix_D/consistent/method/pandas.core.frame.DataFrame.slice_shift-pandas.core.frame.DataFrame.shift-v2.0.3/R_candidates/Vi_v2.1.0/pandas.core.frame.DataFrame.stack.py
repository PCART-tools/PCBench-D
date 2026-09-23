    def stack(
        self,
        level: IndexLabel = -1,
        dropna: bool | lib.NoDefault = lib.no_default,
        sort: bool | lib.NoDefault = lib.no_default,
        future_stack: bool = False,
    ):
        """
        Stack the prescribed level(s) from columns to index.

        Return a reshaped DataFrame or Series having a multi-level
        index with one or more new inner-most levels compared to the current
        DataFrame. The new inner-most levels are created by pivoting the
        columns of the current dataframe:

          - if the columns have a single level, the output is a Series;
          - if the columns have multiple levels, the new index
            level(s) is (are) taken from the prescribed level(s) and
            the output is a DataFrame.

        Parameters
        ----------
        level : int, str, list, default -1
            Level(s) to stack from the column axis onto the index
            axis, defined as one index or label, or a list of indices
            or labels.
        dropna : bool, default True
            Whether to drop rows in the resulting Frame/Series with
            missing values. Stacking a column level onto the index
            axis can create combinations of index and column values
            that are missing from the original dataframe. See Examples
            section.
        sort : bool, default True
            Whether to sort the levels of the resulting MultiIndex.
        future_stack : bool, default False
            Whether to use the new implementation that will replace the current
            implementation in pandas 3.0. When True, dropna and sort have no impact
            on the result and must remain unspecified. See :ref:`pandas 2.1.0 Release
            notes <whatsnew_210.enhancements.new_stack>` for more details.

        Returns
        -------
        DataFrame or Series
            Stacked dataframe or series.

        See Also
        --------
        DataFrame.unstack : Unstack prescribed level(s) from index axis
             onto column axis.
        DataFrame.pivot : Reshape dataframe from long format to wide
             format.
        DataFrame.pivot_table : Create a spreadsheet-style pivot table
             as a DataFrame.

        Notes
        -----
        The function is named by analogy with a collection of books
        being reorganized from being side by side on a horizontal
        position (the columns of the dataframe) to being stacked
        vertically on top of each other (in the index of the
        dataframe).

        Reference :ref:`the user guide <reshaping.stacking>` for more examples.

        Examples
        --------
        **Single level columns**

        >>> df_single_level_cols = pd.DataFrame([[0, 1], [2, 3]],
        ...                                     index=['cat', 'dog'],
        ...                                     columns=['weight', 'height'])

        Stacking a dataframe with a single level column axis returns a Series:

        >>> df_single_level_cols
             weight height
        cat       0      1
        dog       2      3
        >>> df_single_level_cols.stack(future_stack=True)
        cat  weight    0
             height    1
        dog  weight    2
             height    3
        dtype: int64

        **Multi level columns: simple case**

        >>> multicol1 = pd.MultiIndex.from_tuples([('weight', 'kg'),
        ...                                        ('weight', 'pounds')])
        >>> df_multi_level_cols1 = pd.DataFrame([[1, 2], [2, 4]],
        ...                                     index=['cat', 'dog'],
        ...                                     columns=multicol1)

        Stacking a dataframe with a multi-level column axis:

        >>> df_multi_level_cols1
             weight
                 kg    pounds
        cat       1        2
        dog       2        4
        >>> df_multi_level_cols1.stack(future_stack=True)
                    weight
        cat kg           1
            pounds       2
        dog kg           2
            pounds       4

        **Missing values**

        >>> multicol2 = pd.MultiIndex.from_tuples([('weight', 'kg'),
        ...                                        ('height', 'm')])
        >>> df_multi_level_cols2 = pd.DataFrame([[1.0, 2.0], [3.0, 4.0]],
        ...                                     index=['cat', 'dog'],
        ...                                     columns=multicol2)

        It is common to have missing values when stacking a dataframe
        with multi-level columns, as the stacked dataframe typically
        has more values than the original dataframe. Missing values
        are filled with NaNs:

        >>> df_multi_level_cols2
            weight height
                kg      m
        cat    1.0    2.0
        dog    3.0    4.0
        >>> df_multi_level_cols2.stack(future_stack=True)
                weight  height
        cat kg     1.0     NaN
            m      NaN     2.0
        dog kg     3.0     NaN
            m      NaN     4.0

        **Prescribing the level(s) to be stacked**

        The first parameter controls which level or levels are stacked:

        >>> df_multi_level_cols2.stack(0, future_stack=True)
                     kg    m
        cat weight  1.0  NaN
            height  NaN  2.0
        dog weight  3.0  NaN
            height  NaN  4.0
        >>> df_multi_level_cols2.stack([0, 1], future_stack=True)
        cat  weight  kg    1.0
             height  m     2.0
        dog  weight  kg    3.0
             height  m     4.0
        dtype: float64

        **Dropping missing values**

        >>> df_multi_level_cols3 = pd.DataFrame([[None, 1.0], [2.0, 3.0]],
        ...                                     index=['cat', 'dog'],
        ...                                     columns=multicol2)

        Note that rows where all values are missing are dropped by
        default but this behaviour can be controlled via the dropna
        keyword parameter:

        >>> df_multi_level_cols3
            weight height
                kg      m
        cat    NaN    1.0
        dog    2.0    3.0
        >>> df_multi_level_cols3.stack(dropna=False)
                weight  height
        cat kg     NaN     NaN
            m      NaN     1.0
        dog kg     2.0     NaN
            m      NaN     3.0
        >>> df_multi_level_cols3.stack(dropna=True)
                weight  height
        cat m      NaN     1.0
        dog kg     2.0     NaN
            m      NaN     3.0
        """
        if not future_stack:
            from pandas.core.reshape.reshape import (
                stack,
                stack_multiple,
            )

            if dropna is lib.no_default:
                dropna = True
            if sort is lib.no_default:
                sort = True

            if isinstance(level, (tuple, list)):
                result = stack_multiple(self, level, dropna=dropna, sort=sort)
            else:
                result = stack(self, level, dropna=dropna, sort=sort)
        else:
            from pandas.core.reshape.reshape import stack_v3

            if dropna is not lib.no_default:
                raise ValueError(
                    "dropna must be unspecified with future_stack=True as the new "
                    "implementation does not introduce rows of NA values. This "
                    "argument will be removed in a future version of pandas."
                )

            if sort is not lib.no_default:
                raise ValueError(
                    "Cannot specify sort with future_stack=True, this argument will be "
                    "removed in a future version of pandas. Sort the result using "
                    ".sort_index instead."
                )

            if (
                isinstance(level, (tuple, list))
                and not all(lev in self.columns.names for lev in level)
                and not all(isinstance(lev, int) for lev in level)
            ):
                raise ValueError(
                    "level should contain all level names or all level "
                    "numbers, not a mixture of the two."
                )

            if not isinstance(level, (tuple, list)):
                level = [level]
            level = [self.columns._get_level_number(lev) for lev in level]
            result = stack_v3(self, level)

        return result.__finalize__(self, method="stack")
