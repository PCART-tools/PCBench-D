    def open_text_files(path, encoding=system_encoding, errors='strict'):
        """ Open many files in text mode.  Return delayed objects.

        See Also
        --------
        dask.bytes.core.open_text_files: User function
        """
        myopen = delayed(open)
        filepaths = sorted(glob(path))
        return [myopen(_path, encoding=encoding, errors=errors,
                       dask_key_name='open-%s'
                                     % tokenize(_path,
                                                encoding,
                                                errors,
                                                os.path.getmtime(_path)))
                for _path in filepaths]
