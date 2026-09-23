def get_chrome_trace_events(filename):
    f = open(filename)
    data = json.load(f)
    events = data["traceEvents"]
    return events
