def _wraps(
    fun: Optional[Callable[..., Any]],
    update_doc: bool = True,
    lax_description: str = "",
    sections: Sequence[str] = ('Parameters', 'Returns', 'References'),
    skip_params: Sequence[str] = (),
    extra_params: Optional[str] = None,
    module: Optional[str] = None,
) -> Callable[[_T], _T]:
  """Specialized version of functools.wraps for wrapping numpy functions.

  This produces a wrapped function with a modified docstring. In particular, if
  `update_doc` is True, parameters listed in the wrapped function that are not
  supported by the decorated function will be removed from the docstring. For
  this reason, it is important that parameter names match those in the original
  numpy function.

  Args:
    fun: The function being wrapped
    update_doc: whether to transform the numpy docstring to remove references of
      parameters that are supported by the numpy version but not the JAX version.
      If False, include the numpy docstring verbatim.
    lax_description: a string description that will be added to the beginning of
      the docstring.
    sections: a list of sections to include in the docstring. The default is
      ["Parameters", "returns", "References"]
    skip_params: a list of strings containing names of parameters accepted by the
      function that should be skipped in the parameter list.
    extra_params: an optional string containing additional parameter descriptions.
      When ``update_doc=True``, these will be added to the list of parameter
      descriptions in the updated doc.
    module: an optional string specifying the module from which the wrapped function
      is imported. This is useful for objects such as ufuncs, where the module cannot
      be determined from the wrapped function itself.
  """
  def wrap(op):
    op.__np_wrapped__ = fun
    # Allows this pattern: @wraps(getattr(np, 'new_function', None))
    if fun is None:
      return op
    docstr = getattr(fun, "__doc__", None)
    name = getattr(fun, "__name__", getattr(op, "__name__", str(op)))
    try:
      mod = module or fun.__module__
    except AttributeError:
      if config.jax_enable_checks:
        raise ValueError(f"function {fun} defines no __module__; pass module keyword to _wraps.")
    else:
      name = f"{mod}.{name}"
    if docstr:
      try:
        parsed = _parse_numpydoc(docstr)

        if update_doc and 'Parameters' in parsed.sections:
          code = getattr(getattr(op, "__wrapped__", op), "__code__", None)
          # Remove unrecognized parameter descriptions.
          parameters = _parse_parameters(parsed.sections['Parameters'])
          if extra_params:
            parameters.update(_parse_extra_params(extra_params))
          parameters = {p: desc for p, desc in parameters.items()
                        if (code is None or p in code.co_varnames)
                        and p not in skip_params}
          if parameters:
            parsed.sections['Parameters'] = (
              "Parameters\n"
              "----------\n" +
              "\n".join(_versionadded.split(desc)[0].rstrip()
                        for p, desc in parameters.items())
            )
          else:
            del parsed.sections['Parameters']

        docstr = parsed.summary.strip() + "\n" if parsed.summary else ""
        docstr += f"\nLAX-backend implementation of :func:`{name}`.\n"
        if lax_description:
          docstr += "\n" + lax_description.strip() + "\n"
        docstr += "\n*Original docstring below.*\n"

        # We remove signatures from the docstrings, because they redundant at best and
        # misleading at worst: e.g. JAX wrappers don't implement all ufunc keyword arguments.
        # if parsed.signature:
        #   docstr += "\n" + parsed.signature.strip() + "\n"

        if parsed.front_matter:
          docstr += "\n" + parsed.front_matter.strip() + "\n"
        kept_sections = (content.strip() for section, content in parsed.sections.items()
                         if section in sections)
        if kept_sections:
          docstr += "\n" + "\n\n".join(kept_sections) + "\n"
      except:
        if config.jax_enable_checks:
          raise
        docstr = fun.__doc__

    op.__doc__ = docstr
    for attr in ['__name__', '__qualname__']:
      try:
        value = getattr(fun, attr)
      except AttributeError:
        pass
      else:
        setattr(op, attr, value)
    return op
  return wrap
