def _getitem(self, item):
  return lax_numpy._rewriting_take(self, item)
