def update_diff_guard_managers_for_existing_cache_entries(cache_entry):
    first_cache_entry = cache_entry

    # On the first pass, go through the cache entries and accumulate the diff
    # guard sources. Different guard managers can fail with different sources.
    # So, we collect all of them first.
    acc_diff_guard_sources = set()
    while cache_entry is not None:
        acc_diff_guard_sources.update(
            cache_entry.guard_manager.collect_diff_guard_sources()
        )
        cache_entry = cache_entry.next

    # On the second pass, set the diff_guard_sources for each cache line to the
    # accumulated value. And the re-populate the diff guard manager.
    cache_entry = first_cache_entry
    while cache_entry is not None:
        cache_entry.guard_manager.diff_guard_sources = acc_diff_guard_sources
        cache_entry.guard_manager.populate_diff_guard_manager()
        cache_entry = cache_entry.next

    # return the accumulated sources to set up the new cache line.
    return acc_diff_guard_sources
