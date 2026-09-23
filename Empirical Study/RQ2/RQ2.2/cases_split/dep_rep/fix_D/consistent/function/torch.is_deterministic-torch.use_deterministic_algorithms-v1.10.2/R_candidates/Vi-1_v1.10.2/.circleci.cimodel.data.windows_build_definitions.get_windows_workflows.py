def get_windows_workflows():
    return [item.gen_tree() for item in WORKFLOW_DATA]
