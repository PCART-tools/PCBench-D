def build_message(size: int) -> Dict[str, Any]:
    build_env_split: List[Any] = os.environ.get("BUILD_ENVIRONMENT", "").split()
    pkg_type, py_ver, cu_ver, *_ = build_env_split + [None, None, None]
    os_name = os.uname()[0].lower()
    if os_name == "darwin":
        os_name = "macos"

    return {
        "normal": {
            "os": os_name,
            "pkg_type": pkg_type,
            "py_ver": py_ver,
            "cu_ver": cu_ver,
            "pr": os.environ.get("CIRCLE_PR_NUMBER"),
            "build_num": os.environ.get("CIRCLE_BUILD_NUM"),
            "sha1": os.environ.get("CIRCLE_SHA1"),
            "branch": os.environ.get("CIRCLE_BRANCH"),
            "workflow_id": os.environ.get("CIRCLE_WORKFLOW_ID"),
        },
        "int": {
            "time": int(time.time()),
            "size": size,
            "commit_time": int(os.environ.get("COMMIT_TIME", "0")),
            "run_duration": int(
                time.time() - os.path.getmtime(os.path.realpath(__file__))
            ),
        },
    }
