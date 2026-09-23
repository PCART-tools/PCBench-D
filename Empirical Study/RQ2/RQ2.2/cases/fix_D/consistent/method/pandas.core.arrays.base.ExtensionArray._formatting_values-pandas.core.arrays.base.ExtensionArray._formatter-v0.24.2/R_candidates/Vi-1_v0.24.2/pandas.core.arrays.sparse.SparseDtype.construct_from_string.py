    @classmethod
    def construct_from_string(cls, string):
        """
        Construct a SparseDtype from a string form.

        Parameters
        ----------
        string : str
            Can take the following forms.

            string           dtype
            ================ ============================
            'int'            SparseDtype[np.int64, 0]
            'Sparse'         SparseDtype[np.float64, nan]
            'Sparse[int]'    SparseDtype[np.int64, 0]
            'Sparse[int, 0]' SparseDtype[np.int64, 0]
            ================ ============================

            It is not possible to specify non-default fill values
            with a string. An argument like ``'Sparse[int, 1]'``
            will raise a ``TypeError`` because the default fill value
            for integers is 0.

        Returns
        -------
        SparseDtype
        """
        msg = "Could not construct SparseDtype from '{}'".format(string)
        if string.startswith("Sparse"):
            try:
                sub_type, has_fill_value = cls._parse_subtype(string)
                result = SparseDtype(sub_type)
            except Exception:
                raise TypeError(msg)
            else:
                msg = ("Could not construct SparseDtype from '{}'.\n\nIt "
                       "looks like the fill_value in the string is not "
                       "the default for the dtype. Non-default fill_values "
                       "are not supported. Use the 'SparseDtype()' "
                       "constructor instead.")
                if has_fill_value and str(result) != string:
                    raise TypeError(msg.format(string))
                return result
        else:
            raise TypeError(msg)
