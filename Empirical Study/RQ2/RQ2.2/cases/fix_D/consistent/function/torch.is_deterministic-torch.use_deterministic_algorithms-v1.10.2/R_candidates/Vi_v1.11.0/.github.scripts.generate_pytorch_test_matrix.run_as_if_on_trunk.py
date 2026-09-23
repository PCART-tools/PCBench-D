def run_as_if_on_trunk() -> bool:
    ON_PULL_REQUEST = os.getenv('GITHUB_HEAD_REF')
    if not ON_PULL_REQUEST:
        return True

    from pathlib import Path
    GITHUB_DIR = Path(__file__).resolve().parent.parent

    with open(f'{GITHUB_DIR}/generated-ciflow-ruleset.json') as f:
        labels_to_workflows = json.load(f)['label_rules']

    pr_labels = json.loads(os.getenv('PR_LABELS', '[]'))
    current_workflow_triggered_by_label = False
    for label in pr_labels:
        if label != 'ciflow/default' and label in labels_to_workflows:
            workflows_triggered_by_label = labels_to_workflows[label]
            if any([BUILD_ENVIRONMENT in workflow for workflow in workflows_triggered_by_label]):
                current_workflow_triggered_by_label = True
                break

    return current_workflow_triggered_by_label
