def implements(
    original_fun: Callable[..., Any] | None,
    update_doc: bool = True,
    lax_description: str = "",
    sections: Sequence[str] = ('Parameters', 'Returns', 'References'),
    skip_params: Sequence[str] = (),
    module: str | None = None,
) -> Callable[[_T], _T]:
  """Decorator for JAX functions which implement a specified NumPy function.

  This mainly contains logic to copy and modify the docstring of the original
  function. In particular, if `update_doc` is True, parameters listed in the
  original function that are not supported by the decorated function will
  be removed from the docstring. For this reason, it is important that parameter
  names match those in the original numpy function.

  Args:
    original_fun: The original function being implemented
    update_doc: whether to transform the numpy docstring to remove references of
      parameters that are supported by the numpy version but not the JAX version.
      If False, include the numpy docstring verbatim.
    lax_description: a string description that will be added to the beginning of
      the docstring.
    sections: a list of sections to include in the docstring. The default is
      ["Parameters", "Returns", "References"]
    skip_params: a list of strings containing names of parameters accepted by the
      function that should be skipped in the parameter list.
    module: an optional string specifying the module from which the original function
      is imported. This is useful for objects such as ufuncs, where the module cannot
      be determined from the original function itself.
  """
  def decorator(wrapped_fun):
    wrapped_fun.__np_wrapped__ = original_fun
    # Allows this pattern: @implements(getattr(np, 'new_function', None))
    if original_fun is None:
      if lax_description:
        wrapped_fun.__doc__ = lax_description
      return wrapped_fun
    docstr = getattr(original_fun, "__doc__", None)
    name = getattr(original_fun, "__name__", getattr(wrapped_fun, "__name__", str(wrapped_fun)))
    try:
      mod = module or original_fun.__module__
    except AttributeError:
      if config.enable_checks.value:
        raise ValueError(f"function {original_fun} defines no __module__; pass module keyword to implements().")
    else:
      name = f"{mod}.{name}"
    if docstr:
      try:
        parsed = _parse_numpydoc(docstr)

        if update_doc and 'Parameters' in parsed.sections:
          code = getattr(getattr(wrapped_fun, "__wrapped__", wrapped_fun), "__code__", None)
          # Remove unrecognized parameter descriptions.
          parameters = _parse_parameters(parsed.sections['Parameters'])
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
        if config.enable_checks.value:
          raise
        docstr = original_fun.__doc__

    wrapped_fun.__doc__ = docstr
    for attr in ['__name__', '__qualname__']:
      try:
        value = getattr(original_fun, attr)
      except AttributeError:
        pass
      else:
        setattr(wrapped_fun, attr, value)
    return wrapped_fun
  return decorator
