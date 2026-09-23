def rem(lhs, rhs):
  return np.sign(lhs) * np.remainder(np.abs(lhs), np.abs(rhs))
