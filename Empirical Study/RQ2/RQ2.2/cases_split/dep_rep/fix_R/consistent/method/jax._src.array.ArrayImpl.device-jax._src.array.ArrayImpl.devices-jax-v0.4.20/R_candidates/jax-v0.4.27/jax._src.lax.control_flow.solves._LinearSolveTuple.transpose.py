  def transpose(self):
    return type(self)(self.vecmat, self.matvec, self.transpose_solve, self.solve)
