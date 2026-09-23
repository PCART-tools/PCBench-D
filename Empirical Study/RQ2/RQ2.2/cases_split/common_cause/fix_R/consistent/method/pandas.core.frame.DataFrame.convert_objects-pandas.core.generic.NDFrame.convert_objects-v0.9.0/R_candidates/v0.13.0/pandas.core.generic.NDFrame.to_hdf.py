    def to_hdf(self, path_or_buf, key, **kwargs):
        """ activate the HDFStore

        Parameters
        ----------
        path_or_buf : the path (string) or buffer to put the store
        key : string, an indentifier for the group in the store
        mode : optional, {'a', 'w', 'r', 'r+'}, default 'a'

          ``'r'``
              Read-only; no data can be modified.
          ``'w'``
              Write; a new file is created (an existing file with the same
              name would be deleted).
          ``'a'``
              Append; an existing file is opened for reading and writing,
              and if the file does not exist it is created.
          ``'r+'``
              It is similar to ``'a'``, but the file must already exist.
        format   : 'fixed(f)|table(t)', default is 'fixed'
            fixed(f) : Fixed format
                       Fast writing/reading. Not-appendable, nor searchable
            table(t) : Table format
                       Write as a PyTables Table structure which may perform
                       worse but allow more flexible operations like searching
                       / selecting subsets of the data
        append   : boolean, default False
            For Table formats, append the input data to the existing
        complevel : int, 1-9, default 0
            If a complib is specified compression will be applied
            where possible
        complib : {'zlib', 'bzip2', 'lzo', 'blosc', None}, default None
            If complevel is > 0 apply compression to objects written
            in the store wherever possible
        fletcher32 : bool, default False
            If applying compression use the fletcher32 checksum

        """

        from pandas.io import pytables
        return pytables.to_hdf(path_or_buf, key, self, **kwargs)
