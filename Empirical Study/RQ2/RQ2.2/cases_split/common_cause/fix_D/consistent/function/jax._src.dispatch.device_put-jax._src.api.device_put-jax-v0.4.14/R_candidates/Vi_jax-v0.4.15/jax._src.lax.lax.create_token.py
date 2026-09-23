def create_token(_=None):
  """Creates an XLA token value with no preconditions for sequencing effects.

  Experimental.

  The argument is ignored. It exists for backward compatibility.
  """
  return create_token_p.bind()
