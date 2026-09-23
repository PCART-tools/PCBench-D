    @classmethod
    def _from_dict(
        cls,
        data: Mapping[str, Sequence[object] | Mapping[str, Sequence[object]] | Series],
        schema: SchemaDefinition | None = None,
        *,
        schema_overrides: SchemaDict | None = None,
    ) -> Self:
        """
        Construct a DataFrame from a dictionary of sequences.

        Parameters
        ----------
        data : dict of sequences
          Two-dimensional data represented as a dictionary. dict must contain
          Sequences.
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

        """
        return cls._from_pydf(
            dict_to_pydf(data, schema=schema, schema_overrides=schema_overrides)
        )
