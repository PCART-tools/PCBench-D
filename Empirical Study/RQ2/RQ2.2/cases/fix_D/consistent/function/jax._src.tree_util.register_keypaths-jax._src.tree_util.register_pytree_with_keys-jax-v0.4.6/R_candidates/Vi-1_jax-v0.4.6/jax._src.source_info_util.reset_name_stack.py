@contextlib.contextmanager
def reset_name_stack() -> Iterator[None]:
  with set_name_stack(NameStack()):
    yield
