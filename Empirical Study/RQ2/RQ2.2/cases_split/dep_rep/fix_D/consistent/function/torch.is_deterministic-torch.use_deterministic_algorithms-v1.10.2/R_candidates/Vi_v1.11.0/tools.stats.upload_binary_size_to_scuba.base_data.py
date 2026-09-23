def base_data() -> Dict[str, Any]:
    return {
        "run_duration_seconds": int(
            time.time() - os.path.getmtime(os.path.realpath(__file__))
        ),
    }
