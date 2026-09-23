@Printer.register(Task)
def print_task(text, task):
    outs = ', '.join(_print_task_output(o) for o in task.outputs())
    context = [('node', task.node), ('name', task.name), ('outputs', outs)]
    with text.context(call('Task', context)):
        text(task.get_step())
