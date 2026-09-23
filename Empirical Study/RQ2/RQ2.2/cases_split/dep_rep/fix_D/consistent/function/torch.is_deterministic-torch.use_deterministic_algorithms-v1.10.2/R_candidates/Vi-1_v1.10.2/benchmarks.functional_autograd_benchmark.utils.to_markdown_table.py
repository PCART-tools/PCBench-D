def to_markdown_table(res: TimingResultType, header: Tuple[str, ...] = None) -> str:
    if header is None:
        header = ("model", "task", "mean", "var")
    out = ""

    def write_line(*args):
        nonlocal out
        out += "| {} |\n".format(" | ".join(str(a) for a in args))

    # Make it a markdown table
    write_line(*header)
    write_line(*["--"] * len(header))
    for model, tasks in res.items():
        for task, line in tasks.items():
            write_line(*(model, task) + line)

    return out
