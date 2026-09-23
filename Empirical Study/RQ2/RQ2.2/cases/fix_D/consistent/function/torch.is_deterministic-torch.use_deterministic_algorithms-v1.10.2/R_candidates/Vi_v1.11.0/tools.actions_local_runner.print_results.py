def print_results(job_name: str, passed: bool, streams: List[str]) -> None:
    icon = color(col.GREEN, "✓") if passed else color(col.RED, "x")
    print(f"{icon} {color(col.BLUE, job_name)}")

    for stream in streams:
        stream = stream.strip()
        if stream != "":
            print(stream)
