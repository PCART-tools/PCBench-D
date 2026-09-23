    @classmethod
    def _from_arrow(
        cls,
        data: pa.Table | pa.RecordBatch,
        schema: SchemaDefinition | None = None,
        *,
        schema_overrides: SchemaDict | None = None,
        rechunk: bool = True,
    ) -> DataFrame:
        """
        Construct a DataFrame from an Arrow table.

        This operation will be zero copy for the most part. Types that are not
        supported by Polars may be cast to the closest supported type.

        Parameters
        ----------
        data : arrow Table, RecordBatch, or sequence of sequences
            Data representing an Arrow Table or RecordBatch.
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
        rechunk : bool, default True
            Make sure that all data is in contiguous memory.
        """
        return cls._from_pydf(
            arrow_to_pydf(
                data,
                schema=schema,
                schema_overrides=schema_overrides,
                rechunk=rechunk,
            )
        )
