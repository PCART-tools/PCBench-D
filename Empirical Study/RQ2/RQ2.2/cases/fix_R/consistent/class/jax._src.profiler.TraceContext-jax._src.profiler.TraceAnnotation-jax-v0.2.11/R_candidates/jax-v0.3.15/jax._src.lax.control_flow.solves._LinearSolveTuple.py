class _LinearSolveTuple(collections.namedtuple(
    '_LinearSolveTuple', 'matvec, vecmat, solve, transpose_solve')):

  def transpose(self):
    return type(self)(self.vecmat, self.matvec, self.transpose_solve, self.solve)
