@contextlib.contextmanager
def serial_loop(name: ResourceAxisName, length: int):
  """Define a serial loop resource to be available in scope of this context manager.

  This is similar to :py:class:`Mesh` in that it extends the resource
  environment with a resource called ``name``. But, any use of this resource
  axis in ``axis_resources`` argument of :py:func:`xmap` will cause the
  body of :py:func:`xmap` to get executed ``length`` times with each execution
  only processing only a slice of inputs mapped along logical axes assigned
  to this resource.

  This is especially useful in that it makes it possible to lower the memory
  usage compared to :py:func:`vmap`, because it will avoid simultaneous
  materialization of intermediate values for every point in the batch.

  Note that collectives over loop axes are not supported, so they are less
  versatile than physical mesh axes.

  Args:
    name: Name of the loop in the resource environment.
    length: Number of iterations.

  Example::

    with loop('l', 4):
      out = xmap(
        lambda x: jnp.sin(x) * 5,  # This will be called 4 times with different
                                   # slices of x.
        in_axes=['i'], out_axes=['i'],
        axis_resources={'i': 'l'})(x)
  """
  old_env: ResourceEnv = getattr(thread_resources, "env", EMPTY_ENV)
  thread_resources.env = old_env.with_extra_loop(mesh.Loop(name, length))
  try:
    yield
  finally:
    thread_resources.env = old_env
