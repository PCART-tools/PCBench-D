    def assign(self, **kwargs):
        r"""
        Assign new columns to a DataFrame.

        Returns a new object with all original columns in addition to new ones.
        Existing columns that are re-assigned will be overwritten.

        Parameters
        ----------
        **kwargs : dict of {str: callable or Series}
            The column names are keywords. If the values are
            callable, they are computed on the DataFrame and
            assigned to the new columns. The callable must not
            change input DataFrame (though pandas doesn't check it).
            If the values are not callable, (e.g. a Series, scalar, or array),
            they are simply assigned.

        Returns
        -------
        DataFrame
            A new DataFrame with the new columns in addition to
            all the existing columns.

        Notes
        -----
        Assigning multiple columns within the same ``assign`` is possible.
        For Python 3.6 and above, later items in '\*\*kwargs' may refer to
        newly created or modified columns in 'df'; items are computed and
        assigned into 'df' in order.  For Python 3.5 and below, the order of
        keyword arguments is not specified, you cannot refer to newly created
        or modified columns. All items are computed first, and then assigned
        in alphabetical order.

        .. versionchanged :: 0.23.0

           Keyword argument order is maintained for Python 3.6 and later.

        Examples
        --------
        >>> df = pd.DataFrame({'temp_c': [17.0, 25.0]},
        ...                   index=['Portland', 'Berkeley'])
        >>> df
                  temp_c
        Portland    17.0
        Berkeley    25.0

        Where the value is a callable, evaluated on `df`:

        >>> df.assign(temp_f=lambda x: x.temp_c * 9 / 5 + 32)
                  temp_c  temp_f
        Portland    17.0    62.6
        Berkeley    25.0    77.0

        Alternatively, the same behavior can be achieved by directly
        referencing an existing Series or sequence:

        >>> df.assign(temp_f=df['temp_c'] * 9 / 5 + 32)
                  temp_c  temp_f
        Portland    17.0    62.6
        Berkeley    25.0    77.0

        In Python 3.6+, you can create multiple columns within the same assign
        where one of the columns depends on another one defined within the same
        assign:

        >>> df.assign(temp_f=lambda x: x['temp_c'] * 9 / 5 + 32,
        ...           temp_k=lambda x: (x['temp_f'] +  459.67) * 5 / 9)
                  temp_c  temp_f  temp_k
        Portland    17.0    62.6  290.15
        Berkeley    25.0    77.0  298.15
        """
        data = self.copy()

        # >= 3.6 preserve order of kwargs
        if PY36:
            for k, v in kwargs.items():
                data[k] = com.apply_if_callable(v, data)
        else:
            # <= 3.5: do all calculations first...
            results = OrderedDict()
            for k, v in kwargs.items():
                results[k] = com.apply_if_callable(v, data)

            # <= 3.5 and earlier
            results = sorted(results.items())
            # ... and then assign
            for k, v in results:
                data[k] = v
        return data
