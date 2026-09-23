    @final
    @doc(
        storage_options=_shared_docs["storage_options"],
        compression_options=_shared_docs["compression_options"] % "path",
    )
    def to_pickle(
        self,
        path: FilePath | WriteBuffer[bytes],
        compression: CompressionOptions = "infer",
        protocol: int = pickle.HIGHEST_PROTOCOL,
        storage_options: StorageOptions | None = None,
    ) -> None:
        """
        Pickle (serialize) object to file.

        Parameters
        ----------
        path : str, path object, or file-like object
            String, path object (implementing ``os.PathLike[str]``), or file-like
            object implementing a binary ``write()`` function. File path where
            the pickled object will be stored.
        {compression_options}
        protocol : int
            Int which indicates which protocol should be used by the pickler,
            default HIGHEST_PROTOCOL (see [1]_ paragraph 12.1.2). The possible
            values are 0, 1, 2, 3, 4, 5. A negative value for the protocol
            parameter is equivalent to setting its value to HIGHEST_PROTOCOL.

            .. [1] https://docs.python.org/3/library/pickle.html.

        {storage_options}

            .. versionadded:: 1.2.0

        See Also
        --------
        read_pickle : Load pickled pandas object (or any object) from file.
        DataFrame.to_hdf : Write DataFrame to an HDF5 file.
        DataFrame.to_sql : Write DataFrame to a SQL database.
        DataFrame.to_parquet : Write a DataFrame to the binary parquet format.

        Examples
        --------
        >>> original_df = pd.DataFrame({{"foo": range(5), "bar": range(5, 10)}})  # doctest: +SKIP
        >>> original_df  # doctest: +SKIP
           foo  bar
        0    0    5
        1    1    6
        2    2    7
        3    3    8
        4    4    9
        >>> original_df.to_pickle("./dummy.pkl")  # doctest: +SKIP

        >>> unpickled_df = pd.read_pickle("./dummy.pkl")  # doctest: +SKIP
        >>> unpickled_df  # doctest: +SKIP
           foo  bar
        0    0    5
        1    1    6
        2    2    7
        3    3    8
        4    4    9
        """  # noqa: E501
        from pandas.io.pickle import to_pickle

        to_pickle(
            self,
            path,
            compression=compression,
            protocol=protocol,
            storage_options=storage_options,
        )
