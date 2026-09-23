def _check_1d(x):
    """Convert scalars to 1D arrays; pass-through arrays as is."""
    if not hasattr(x, 'shape') or len(x.shape) < 1:
        return np.atleast_1d(x)
    else:
        try:
            # work around
            # https://github.com/pandas-dev/pandas/issues/27775 which
            # means the shape of multi-dimensional slicing is not as
            # expected.  That this ever worked was an unintentional
            # quirk of pandas and will raise an exception in the
            # future.  This slicing warns in pandas >= 1.0rc0 via
            # https://github.com/pandas-dev/pandas/pull/30588
            #
            # < 1.0rc0 : x[:, None].ndim == 1, no warning, custom type
            # >= 1.0rc1 : x[:, None].ndim == 2, warns, numpy array
            # future : x[:, None] -> raises
            #
            # This code should correctly identify and coerce to a
            # numpy array all pandas versions.
            with warnings.catch_warnings(record=True) as w:
                warnings.filterwarnings(
                    "always",
                    category=Warning,
                    message='Support for multi-dimensional indexing')

                ndim = x[:, None].ndim
                # we have definitely hit a pandas index or series object
                # cast to a numpy array.
                if len(w) > 0:
                    return np.asanyarray(x)
            # We have likely hit a pandas object, or at least
            # something where 2D slicing does not result in a 2D
            # object.
            if ndim < 2:
                return np.atleast_1d(x)
            return x
        # In pandas 1.1.0, multidimensional indexing leads to an
        # AssertionError for some Series objects, but should be
        # IndexError as described in
        # https://github.com/pandas-dev/pandas/issues/35527
        except (AssertionError, IndexError, TypeError):
            return np.atleast_1d(x)
