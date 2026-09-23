def scoped_execution_step(name, *args, **kwargs):
    """Same as execution_step() except that the step name is scoped."""
    default_name = ScopedName(name) if name else name
    return execution_step(default_name, *args, **kwargs)
