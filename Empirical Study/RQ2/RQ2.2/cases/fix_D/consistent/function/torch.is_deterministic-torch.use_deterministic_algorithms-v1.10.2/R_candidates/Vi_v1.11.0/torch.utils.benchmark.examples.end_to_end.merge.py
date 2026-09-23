def merge(measurements):
    if not measurements:
        return None

    states = [m.__getstate__() for m in measurements]
    for k in states[0].keys():
        if k in ("number_per_run", "times", "metadata"):
            continue

        assert all(s[k] == states[0][k] for s in states)

    numbers_per_run = {m.number_per_run for m in measurements}
    n = numbers_per_run.pop() if len(numbers_per_run) == 1 else 1

    merged_state = states[0]
    times = [[t / m.number_per_run * n for t in m.times] for m in measurements]
    merged_state["times"] = list(it.chain(*times))
    merged_state["number_per_run"] = n
    merged_state["metadata"] = states[0]["metadata"]
    return Measurement(**merged_state)
