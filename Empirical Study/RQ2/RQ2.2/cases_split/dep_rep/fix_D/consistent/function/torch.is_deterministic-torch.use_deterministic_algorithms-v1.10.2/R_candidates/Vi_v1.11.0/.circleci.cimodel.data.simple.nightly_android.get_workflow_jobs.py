def get_workflow_jobs():
    return [item.gen_tree() for item in WORKFLOW_DATA]
