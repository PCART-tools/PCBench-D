class Harness:
  """Specifies inputs and callable for a test harness.

  See the module docstring for an introduction to harnesses.

  A harness is conceptually a callable and a list of arguments, that together
  exercise a use case. The harness can optionally have additional parameters
  that can be used by the test.

  The arguments are specified through argument descriptors. An argument
  descriptor can be:
    * a numeric value or ndarray, or
    * an instance of ``RandArg(shape, dtype)`` to be used with a PRNG to
    generate random tensor of the given shape and type, or
    * an instance of ``CustomArg(fun)`` to be used with a PRNG, or
    * an instance of ``StaticArg(value)``. Often these are the non-array
      arguments, e.g., a shape.

  The given callable will be passed one argument corresponding to each
  argument descriptor, e.g., `harness.fun(* harness.args_maker(rng))`.
  However, in many applications we only care about the non-static arguments.
  For that purpose, you can use `harness.dyn_fun(*
  harness.dyn_args_maked(rng))`,
  where `harness.dyn_fun` is `harness.fun` specialized to the static arguments.

  For example, a harness for ``lax.take(arr, indices, axis=None)`` may want
  to expose as external (non-static) argument the array and the indices, and
  keep the axis as a static argument (technically specializing the `take` to
  a axis):

    Harness(lax.slice_p,
            f"take_axis={axis}",
            lax.take,
            [RandArg((2, 4), np.float32), np.array([-1, 0, 1]),
            StaticArg(axis)],
            axis=axis)

  Each harness can have a list of Limitations that describe the cases when
  the harness may not be fully implemented.
  """
  # The group name most often is the primitive name.
  group_name: str
  # Descriptive name of the harness, used as a testcase_name. Unique in a group.
  # Will be sanitized to work with -k test filtering.
  name: str
  # The function taking all arguments (static and dynamic).
  fun: Callable
  # Describes how to construct arguments, see the class docstring.
  arg_descriptors: Sequence[ArgDescriptor]
  dtype: DType
  # A set of limitations describing the cases that are not supported or
  # partially implemented in JAX for this harness.
  jax_unimplemented: Sequence[Limitation]
  rng_factory: Callable
  # Carry some arbitrary parameters that the test can access.
  params: dict[str, Any]

  def __init__(self,
               group_name,
               name,
               fun,
               arg_descriptors,
               *,
               dtype,
               rng_factory=jtu.rand_default,
               jax_unimplemented: Sequence[Limitation] = (),
               **params):
    """See class docstring."""
    self.group_name = jtu.sanitize_test_name(group_name)
    self.name = jtu.sanitize_test_name(name)
    self.fullname = self.name if self.group_name is None else f"{self.group_name}_{self.name}"
    self.fun = fun  # type: ignore[assignment]
    self.arg_descriptors = arg_descriptors
    self.rng_factory = rng_factory  # type: ignore[assignment]
    self.jax_unimplemented = jax_unimplemented
    self.dtype = dtype
    self.params = params

  def __str__(self):
    return self.fullname


  def _arg_maker(self, arg_descriptor, rng: Rng):
    if isinstance(arg_descriptor, StaticArg):
      return arg_descriptor.value
    if isinstance(arg_descriptor, RandArg):
      return self.rng_factory(rng)(arg_descriptor.shape, arg_descriptor.dtype)
    if isinstance(arg_descriptor, CustomArg):
      return arg_descriptor.make(rng)

    return arg_descriptor

  def args_maker(self, rng: Rng) -> Sequence:
    """All-argument maker, including the static ones."""
    return [self._arg_maker(ad, rng) for ad in self.arg_descriptors]

  def dyn_args_maker(self, rng: Rng) -> Sequence:
    """A dynamic-argument maker, for use with `dyn_fun`."""
    return [
        self._arg_maker(ad, rng)
        for ad in self.arg_descriptors
        if not isinstance(ad, StaticArg)
    ]

  def dyn_fun(self, *dyn_args):
    """Invokes `fun` given just the dynamic arguments."""
    all_args = self._args_from_dynargs(dyn_args)
    return self.fun(*all_args)

  def _args_from_dynargs(self, dyn_args: Sequence) -> Sequence:
    """All arguments, including the static ones."""
    next_dynamic_argnum = 0
    all_args = []
    for ad in self.arg_descriptors:
      if isinstance(ad, StaticArg):
        all_args.append(ad.value)
      else:
        all_args.append(dyn_args[next_dynamic_argnum])
        next_dynamic_argnum += 1
    return all_args

  def filter(self,
             device_under_test: str,
             *,
             include_jax_unimpl: bool = False,
             one_containing: str | None = None) -> bool:
    if not include_jax_unimpl:
      if any(
          device_under_test in l.devices
          for l in self.jax_unimplemented
          if l.filter(device=device_under_test, dtype=self.dtype)
      ):
        return False

    if one_containing is not None and one_containing not in self.fullname:
      return False
    return True
