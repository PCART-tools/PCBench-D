def for_loop(nsteps: Union[int, Sequence[int]],
             body: Callable[[Array, Ref[S]], None], init_state: S,
             *, reverse: bool = False, unroll: int = 1) -> S:
  """A for-loop combinator that allows read/write semantics in the loop body.

  `for_loop` is a higher-order function that enables writing loops that can be
  staged out in JIT-ted JAX computations. Unlike `jax.lax.fori_loop`, it allows
  mutation in its body using `Ref`s.

  `for_loop` will initialize `Ref`s with the values in `init_state`. Each
  iteration, `body` will be called with the current `Ref`s, which can be read
  from and written to using `ref_get` and `ref_set`.

  `for_loop` is semantically equivalent to the following Python code:

  ```python
  def for_loop(nsteps, body, init_state):
    refs = tree_map(make_ref, init_state)
    for i in range(nsteps):
      body(i, refs)
    return tree_map(ref_get, refs)
  ```

  Args:
    nsteps: Number of iterations
    body: A callable that takes in the iteration number as its first argument
      and `Ref`s corresponding to `init_state` as its second argument.
      `body` is free to read from and write to its `Ref`s. `body` should
       not return anything.
    init_state: A Pytree of JAX-compatible values used to initialize the `Ref`s
      that will be passed into the for loop body.
    unroll: A positive int specifying, in the underlying operation of the
      `for` primitive, how many iterations to unroll within a single iteration
      of a loop. Higher values may speed up execution time at the cost of longer
      compilation time.
  Returns:
    A Pytree of values representing the output of the for loop.
  """
  if unroll < 1:
    raise ValueError("`unroll` must be a positive integer.")
  if isinstance(nsteps, int):
    nsteps = [nsteps]
  if len(nsteps) > 1:
    outer_step, *rest_steps = nsteps
    def wrapped_body(i, refs):
      vals = tree_map(lambda ref: ref_get(ref, ()), refs)
      vals = for_loop(
          rest_steps, functools.partial(body, i), vals, unroll=unroll)
      tree_map(lambda ref, val: ref_set(ref, (), val), refs, vals)
    return for_loop(outer_step, wrapped_body, init_state, unroll=unroll)
  nsteps, = nsteps
  flat_state, state_tree = tree_flatten(init_state)
  state_avals = map(state_utils.val_to_ref_aval, flat_state)
  idx_aval = core.ShapedArray((), jnp.dtype("int32"))
  jaxpr, consts, out_tree = _trace_to_jaxpr_with_refs(
      body, state_tree, [idx_aval, *state_avals])
  if out_tree != tree_structure(None):
    raise Exception("`body` should not return anything.")
  # Remove constvars from jaxpr and turn them into `Ref`s
  jaxpr = _hoist_consts_to_refs(jaxpr)
  which_linear = (False,) * (len(consts) + len(flat_state))
  out_flat = for_p.bind(*consts, *flat_state, jaxpr=jaxpr, nsteps=int(nsteps),
                        reverse=reverse, which_linear=which_linear,
                        unroll=unroll)
  # Consts are `Ref`s so they are both inputs and outputs. We remove them from
  # the outputs.
  out_flat = out_flat[len(consts):]
  return tree_unflatten(state_tree, out_flat)
