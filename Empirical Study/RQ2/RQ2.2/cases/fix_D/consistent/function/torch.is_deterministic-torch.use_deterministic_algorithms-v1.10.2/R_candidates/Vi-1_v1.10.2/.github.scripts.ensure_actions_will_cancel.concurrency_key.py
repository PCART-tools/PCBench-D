def concurrency_key(filename: Path) -> str:
    workflow_name = filename.with_suffix("").name.replace("_", "-")
    if workflow_name.startswith("generated-"):
        workflow_name = workflow_name[len("generated-"):]
    return f"{workflow_name}-${{{{ github.event.pull_request.number || github.sha }}}}" \
        "-${{ github.event_name == 'workflow_dispatch' }}"
