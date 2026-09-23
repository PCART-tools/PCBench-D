    @classmethod
    def _from_numpy(
        cls,
        data: np.ndarray[Any, Any],
        schema: SchemaDefinition | None = None,
        *,
        schema_overrides: SchemaDict | None = None,
        orient: Orientation | None = None,
    ) -> Self:
        """
        Construct a DataFrame from a numpy ndarray.

        Parameters
        ----------
        data : numpy ndarray
            Two-dimensional data represented as a numpy ndarray.
        schema : Sequence of str, (str,DataType) pairs, or a {str:DataType,} dict
            The DataFrame schema may be declared in several ways:

            * As a dict of {name:type} pairs; if type is None, it will be auto-inferred.
            * As a list of column names; in this case types are automatically inferred.
            * As a list of (name,type) pairs; this is equivalent to the dictionary form.

            If you supply a list of column names that does not match the names in the
            underlying data, the names given here will overwrite them. The number
            of names given in the schema should match the underlying data dimensions.
        schema_overrides : dict, default None
            Support type specification or override of one or more columns; note that
            any dtypes inferred from the columns param will be overridden.
        orient : {'col', 'row'}, default None
            Whether to interpret two-dimensional data as columns or as rows. If None,
            the orientation is inferred by matching the columns and data dimensions. If
            this does not yield conclusive results, column orientation is used.

        """
        return cls._from_pydf(
            numpy_to_pydf(
                data, schema=schema, schema_overrides=schema_overrides, orient=orient
            )
        )
