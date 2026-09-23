def eig_impl(operand, *, compute_left_eigenvectors, compute_right_eigenvectors):
  return (
    xla.apply_primitive(eig_p, operand,
                        compute_left_eigenvectors=compute_left_eigenvectors,
                        compute_right_eigenvectors=compute_right_eigenvectors))
