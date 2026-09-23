def _write_error(e: BaseException, error_file: Optional[str]):
    data = {
        "message": {
            "message": f"{type(e).__name__}: {e}",
            "extraInfo": {
                "py_callstack": traceback.format_exc(),
                "timestamp": str(int(time.time())),
            },
        }
    }

    if error_file:
        with open(error_file, "w") as fp:
            json.dump(data, fp)
    else:
        log.error(json.dumps(data, indent=2))
