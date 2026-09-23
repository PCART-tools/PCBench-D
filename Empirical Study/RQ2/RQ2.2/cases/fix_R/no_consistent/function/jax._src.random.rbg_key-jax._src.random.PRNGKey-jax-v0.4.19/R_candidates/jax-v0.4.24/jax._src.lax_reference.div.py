def div(lhs, rhs):
  if dtypes.issubdtype(dtypes.result_type(lhs), np.integer):
    quotient = np.floor_divide(lhs, rhs)
    select = np.logical_and(np.sign(lhs) != np.sign(rhs),
                             np.remainder(lhs, rhs) != 0)
    return np.where(select, quotient + 1, quotient)
  else:
    return np.divide(lhs, rhs)
