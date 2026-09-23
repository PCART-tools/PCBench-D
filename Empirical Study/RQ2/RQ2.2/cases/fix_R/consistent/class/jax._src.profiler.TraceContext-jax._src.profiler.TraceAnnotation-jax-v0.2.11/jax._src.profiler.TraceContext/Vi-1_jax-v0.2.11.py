class TraceContext(xla_client.profiler.TraceMe):
  """Context manager generates a trace event in the profiler.

  The trace event spans the duration of the code enclosed by the context.

  For example:

  >>> import jax, jax.numpy as jnp
  >>> x = jnp.ones((1000, 1000))
  >>> with jax.profiler.TraceContext("acontext"):
  ...   jnp.dot(x, x.T).block_until_ready()

  This will cause an "acontext" event to show up on the trace timeline if the
  event occurs while the process is being traced by TensorBoard.
  """
  pass
