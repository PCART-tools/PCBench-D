def check_backend_matches(inner_backend, outer_backend):
  # For nested calls, the outermost call sets the backend for all inner calls;
  # it's an error if the inner call has a conflicting explicit backend spec.
  if inner_backend is None:
    return
  if (inner_backend != outer_backend and
      outer_backend not in xb.expand_platform_alias(inner_backend)):
    raise ValueError(
        f"Outer-jit backend specification {outer_backend} must match explicit "
        f"inner-jit backend specification {inner_backend}.")
