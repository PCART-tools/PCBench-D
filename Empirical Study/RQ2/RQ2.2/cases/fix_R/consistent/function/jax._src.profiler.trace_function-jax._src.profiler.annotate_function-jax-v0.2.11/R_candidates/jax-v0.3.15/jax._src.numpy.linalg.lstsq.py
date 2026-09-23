@_wraps(np.linalg.lstsq, lax_description=textwrap.dedent("""\
    It has two important differences:

    1. In `numpy.linalg.lstsq`, the default `rcond` is `-1`, and warns that in the future
       the default will be `None`. Here, the default rcond is `None`.
    2. In `np.linalg.lstsq` the returned residuals are empty for low-rank or over-determined
       solutions. Here, the residuals are returned in all cases, to make the function
       compatible with jit. The non-jit compatible numpy behavior can be recovered by
       passing numpy_resid=True.

    The lstsq function does not currently have a custom JVP rule, so the gradient is
    poorly behaved for some inputs, particularly for low-rank `a`.
    """))
def lstsq(a, b, rcond=None, *, numpy_resid=False):
  if numpy_resid:
    return _lstsq(a, b, rcond, numpy_resid=True)
  return _jit_lstsq(a, b, rcond)
