def unique_process_group_name(prefix):
    # Append timestamp to process group name to make it unique, so
    # that when tests run multiple times or in parallel there
    # wouldn't be name conflicts.
    now = int(time.time() * 1000)
    return "%s_%d" % (prefix, now)
