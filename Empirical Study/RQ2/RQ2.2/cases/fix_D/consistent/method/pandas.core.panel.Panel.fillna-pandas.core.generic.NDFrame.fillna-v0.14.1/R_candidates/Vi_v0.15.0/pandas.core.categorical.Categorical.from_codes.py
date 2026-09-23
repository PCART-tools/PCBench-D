    @classmethod
    def from_codes(cls, codes, categories, ordered=False, name=None):
        """
        Make a Categorical type from codes and categories arrays.

        This constructor is useful if you already have codes and categories and so do not need the
        (computation intensive) factorization step, which is usually done on the constructor.

        If your data does not follow this convention, please use the normal constructor.

        Parameters
        ----------
        codes : array-like, integers
            An integer array, where each integer points to a category in categories or -1 for NaN
        categories : index-like
            The categories for the categorical. Items need to be unique.
        ordered : boolean, optional
            Whether or not this categorical is treated as a ordered categorical. If not given,
            the resulting categorical will be unordered.
        name : str, optional
            Name for the Categorical variable.
        """
        try:
            codes = np.asarray(codes, np.int64)
        except:
            raise ValueError("codes need to be convertible to an arrays of integers")

        categories = cls._validate_categories(categories)

        if codes.max() >= len(categories) or codes.min() < -1:
            raise ValueError("codes need to be between -1 and len(categories)-1")


        return Categorical(codes, categories=categories, ordered=ordered, name=name, fastpath=True)
