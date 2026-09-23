def write_events(tf_dir, events):
    writer = FileWriter(tf_dir, len(events))
    for event in events:
        writer.add_event(event)
    writer.flush()
    writer.close()
