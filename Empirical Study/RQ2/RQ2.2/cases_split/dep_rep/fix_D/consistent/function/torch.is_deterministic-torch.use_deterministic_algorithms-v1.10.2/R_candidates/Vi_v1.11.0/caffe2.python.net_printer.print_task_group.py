@Printer.register(TaskGroup)
def print_task_group(text, tg, header=None):
    with text.context(header or call('TaskGroup')):
        for task in tg.tasks_by_node().tasks():
            text(task)
