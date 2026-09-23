def build_info() -> ReportMetaMeta:
    return {
        "build_pr": os.environ.get("PR_NUMBER", os.environ.get("CIRCLE_PR_NUMBER", "")),
        "build_tag": os.environ.get("TAG", os.environ.get("CIRCLE_TAG", "")),
        "build_sha1": os.environ.get("SHA1", os.environ.get("CIRCLE_SHA1", "")),
        "build_base_commit": get_base_commit(os.environ.get("SHA1", os.environ.get("CIRCLE_SHA1", "HEAD"))),
        "build_branch": os.environ.get("BRANCH", os.environ.get("CIRCLE_BRANCH", "")),
        "build_job": os.environ.get("JOB_BASE_NAME", os.environ.get("CIRCLE_JOB", "")),
        "build_workflow_id": os.environ.get("WORKFLOW_ID", os.environ.get("CIRCLE_WORKFLOW_ID", "")),
        "build_start_time_epoch": str(int(os.path.getmtime(os.path.realpath(__file__)))),
    }
