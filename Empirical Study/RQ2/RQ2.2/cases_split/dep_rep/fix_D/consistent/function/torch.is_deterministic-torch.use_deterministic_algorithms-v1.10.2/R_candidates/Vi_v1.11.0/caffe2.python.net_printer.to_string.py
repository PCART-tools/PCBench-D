def to_string(obj, **kwargs):
    """
    Given a Net, ExecutionStep, Task, TaskGroup or Job, produces a string
    with detailed description of the execution steps.
    """
    printer = Printer(**kwargs)
    printer(obj)
    return str(printer)
