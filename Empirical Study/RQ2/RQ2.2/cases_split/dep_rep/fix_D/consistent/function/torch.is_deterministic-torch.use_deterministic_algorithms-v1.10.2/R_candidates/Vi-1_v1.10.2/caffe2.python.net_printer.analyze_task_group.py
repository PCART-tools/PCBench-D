@Analyzer.register(TaskGroup)
def analyze_task_group(analyzer, tg):
    for task in tg.tasks_by_node().tasks():
        with analyzer.set_workspace(node=task.node):
            analyzer(task)
