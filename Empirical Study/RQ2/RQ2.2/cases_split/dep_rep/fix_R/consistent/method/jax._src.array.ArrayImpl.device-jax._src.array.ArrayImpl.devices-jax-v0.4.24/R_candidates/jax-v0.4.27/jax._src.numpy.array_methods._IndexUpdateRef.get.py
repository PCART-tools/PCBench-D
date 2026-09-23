  def get(self, *, indices_are_sorted=False, unique_indices=False,
          mode=None, fill_value=None):
    """Equivalent to ``x[idx]``.

    Returns the value of ``x`` that would result from the NumPy-style
    :mod:indexing <numpy.doc.indexing>` ``x[idx]``. This function differs from
    the usual array indexing syntax in that it allows additional keyword
    arguments ``indices_are_sorted`` and ``unique_indices`` to be passed.

    See :mod:`jax.ops` for details.
    """
    return lax_numpy._rewriting_take(self.array, self.index,
                                     indices_are_sorted=indices_are_sorted,
                                     unique_indices=unique_indices, mode=mode,
                                     fill_value=fill_value)
