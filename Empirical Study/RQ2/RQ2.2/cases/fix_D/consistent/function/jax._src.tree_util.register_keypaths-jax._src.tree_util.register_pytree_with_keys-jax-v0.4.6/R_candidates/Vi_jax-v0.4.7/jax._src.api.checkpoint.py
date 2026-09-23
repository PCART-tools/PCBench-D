@functools.wraps(new_checkpoint)  # config.jax_new_checkpoint is True by default
def checkpoint(fun: Callable, *,
               concrete: bool = False,
               prevent_cse: bool = True,
               static_argnums: Union[int, Tuple[int, ...]] = (),
               policy: Optional[Callable[..., bool]] = None,
               ) -> Callable:
  if concrete:
    msg = ("The 'concrete' option to jax.checkpoint / jax.remat is deprecated; "
           "in its place, you can use its `static_argnums` option, and if "
           "necessary the `jax.ensure_compile_time_eval()` context manager.\n"
           "\n"
           "For example, if using `concrete=True` for an `is_training` flag:\n"
           "\n"
           "  from functools import partial\n"
           "\n"
           "  @partial(jax.checkpoint, concrete=True)\n"
           "  def foo(x, is_training):\n"
           "    if is_training:\n"
           "      return f(x)\n"
           "    else:\n"
           "      return g(x)\n"
           "\n"
           "replace it with a use of `static_argnums`:\n"
           "\n"
           "  @partial(jax.checkpoint, static_argnums=(1,))\n"
           "  def foo(x, is_training):\n"
           "    ...\n"
           "\n"
           "If jax.numpy operations need to be performed on static arguments, "
           "we can use the `jax.ensure_compile_time_eval()` context manager. "
           "For example, we can replace this use of `concrete=True`\n:"
           "\n"
           "  @partial(jax.checkpoint, concrete=True)\n"
           "  def foo(x, y):\n"
           "    if y > 0:\n"
           "      return f(x)\n"
           "    else:\n"
           "      return g(x)\n"
           "\n"
           "with this combination of `static_argnums` and "
           "`jax.ensure_compile_time_eval()`:\n"
           "\n"
           "  @partial(jax.checkpoint, static_argnums=(1,))\n"
           "  def foo(x, y):\n"
           "    with jax.ensure_compile_time_eval():\n"
           "      y_pos = y > 0\n"
           "    if y_pos:\n"
           "      return f(x)\n"
           "    else:\n"
           "      return g(x)\n"
           "\n"
           "See https://jax.readthedocs.io/en/latest/jep/11830-new-remat-checkpoint.html\n")
    raise NotImplementedError(msg)
  return new_checkpoint(fun, prevent_cse=prevent_cse, policy=policy,
                        static_argnums=static_argnums)
