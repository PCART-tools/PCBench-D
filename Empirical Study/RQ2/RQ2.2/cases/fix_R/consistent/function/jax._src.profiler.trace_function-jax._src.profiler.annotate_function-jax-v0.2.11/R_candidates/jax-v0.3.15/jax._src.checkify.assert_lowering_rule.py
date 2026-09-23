def assert_lowering_rule(*a, **k):
  # TODO(lenamartens): actually throw an error through emit_python_callable
  # TODO(lenamartens) add in-depth error explanation to link to in module docs.
  raise ValueError('Cannot abstractly evaluate a checkify.check which was not'
                   ' functionalized. This probably means you tried to stage'
                   ' (jit/scan/pmap/...) a `check` without functionalizing it'
                   ' through `checkify.checkify`.'
                   )
