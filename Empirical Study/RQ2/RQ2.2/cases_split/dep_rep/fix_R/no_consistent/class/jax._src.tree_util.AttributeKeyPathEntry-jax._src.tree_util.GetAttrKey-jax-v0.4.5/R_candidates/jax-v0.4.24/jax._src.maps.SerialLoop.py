class SerialLoop:
  """Create an anonymous serial loop resource for use in a single xmap axis.

  A use of :py:class:`SerialLoop` in :py:func:`xmap`'s ``axis_resources``
  extends the resource environment with a new serial loop with a unique
  unspecified name, that will only be used to partition the axis that
  used a given instance.

  This is unlike :py:func:`serial_loop`, which makes it possible to iterate
  jointly over chunks of multiple axes (with the usual requirement that they
  do not coincide in a named shape of any value in the program).

  Example::

      # Processes `x` in a vectorized way, but in 20 micro-batches.
      xmap(f, in_axes=['i'], out_axes=[i], axis_resources={'i': SerialLoop(20)})(x)

      # Computes the result in a vectorized way, but in 400 micro-batches,
      # once for each coordinate (0, 0) <= (i, j) < (20, 20). Each `SerialLoop`
      # creates a fresh anonymous loop.
      xmap(h, in_axes=(['i'], ['j']), out_axes=['i', 'j'],
           axis_resources={'i': SerialLoop(20), 'j': SerialLoop(20)})(x, y)
  """
  length: int

  def __init__(self, length):
    self.length = length

  def __eq__(self, other):
    return self.length == other.length

  def __hash__(self):
    return hash(self.length)
