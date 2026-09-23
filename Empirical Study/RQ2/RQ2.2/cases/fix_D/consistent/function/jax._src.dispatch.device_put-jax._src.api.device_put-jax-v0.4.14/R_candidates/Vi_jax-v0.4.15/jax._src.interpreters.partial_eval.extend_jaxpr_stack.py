@contextmanager
def extend_jaxpr_stack(main, frame):
  main.jaxpr_stack = main.jaxpr_stack + (frame,)
  try:
    yield
  finally:
    assert frame is main.jaxpr_stack[-1]
    main.jaxpr_stack = main.jaxpr_stack[:-1]
