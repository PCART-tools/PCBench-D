def _print_task_output(x):
    assert isinstance(x, TaskOutput)
    return 'Output[' + ', '.join(str(x) for x in x.names) + ']'
