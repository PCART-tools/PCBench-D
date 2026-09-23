def from_markdown_table(data: str) -> TimingResultType:
    out = data.strip().split("\n")
    out = out[2:]  # Ignore the header lines

    res: TimingResultType
    res = defaultdict(defaultdict)

    for line in out:
        model, task, mean, var = [f.strip() for f in line.strip().split("|") if f]
        res[model][task] = (float(mean), float(var))

    return res
