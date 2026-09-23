    def to_hdf(self, path_or_buf, key, **kwargs):
        """Write the contained data to an HDF5 file using HDFStore.

        Parameters
        ----------
        path_or_buf : the path (string) or HDFStore object
        key : string
            indentifier for the group in the store
        mode : optional, {'a', 'w', 'r+'}, default 'a'

          ``'w'``
              Write; a new file is created (an existing file with the same
              name would be deleted).
          ``'a'``
              Append; an existing file is opened for reading and writing,
              and if the file does not exist it is created.
          ``'r+'``
              It is similar to ``'a'``, but the file must already exist.
        format : 'fixed(f)|table(t)', default is 'fixed'
            fixed(f) : Fixed format
                       Fast writing/reading. Not-appendable, nor searchable
            table(t) : Table format
                       Write as a PyTables Table structure which may perform
                       worse but allow more flexible operations like searching
                       / selecting subsets of the data
        append : boolean, default False
            For Table formats, append the input data to the existing
        data_columns :  list of columns, or True, default None
            List of columns to create as indexed data columns for on-disk
            queries, or True to use all columns. By default only the axes
            of the object are indexed. See `here
            <http://pandas.pydata.org/pandas-docs/stable/io.html#query-via-data-columns>`__.

            Applicable only to format='table'.
        complevel : int, 1-9, default 0
            If a complib is specified compression will be applied
            where possible
        complib : {'zlib', 'bzip2', 'lzo', 'blosc', None}, default None
            If complevel is > 0 apply compression to objects written
            in the store wherever possible
        fletcher32 : bool, default False
            If applying compression use the fletcher32 checksum
        dropna : boolean, default False.
            If true, ALL nan rows will not be written to store.
        """

        from pandas.io import pytables
        return pytables.to_hdf(path_or_buf, key, self, **kwargs)
