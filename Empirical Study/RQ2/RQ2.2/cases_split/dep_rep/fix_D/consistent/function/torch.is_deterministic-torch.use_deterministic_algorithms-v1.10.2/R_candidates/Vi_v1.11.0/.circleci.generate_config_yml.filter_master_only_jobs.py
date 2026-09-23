def filter_master_only_jobs(items):
    def _is_master_item(item):
        filters = item.get('filters', None)
        branches = filters.get('branches', None) if filters is not None else None
        branches_only = branches.get('only', None) if branches is not None else None
        return 'master' in branches_only if branches_only is not None else False

    master_deps = set()

    def _save_requires_if_master(item_type, item):
        requires = item.get('requires', None)
        item_name = item.get("name", None)
        if not isinstance(requires, list):
            return
        if _is_master_item(item) or item_name in master_deps:
            master_deps.update([n.strip('"') for n in requires])

    def _do_filtering(items):
        if isinstance(items, list):
            rc = [_do_filtering(item) for item in items]
            return [item for item in rc if len(item if item is not None else []) > 0]
        assert isinstance(items, dict) and len(items) == 1
        item_type, item = next(iter(items.items()))
        item_name = item.get("name", None)
        item_name = item_name.strip('"') if item_name is not None else None
        if not _is_master_item(item) and item_name not in master_deps:
            return None
        if 'filters' in item:
            item = item.copy()
            item.pop('filters')
        return {item_type: item}

    # Scan of dependencies twice to pick up nested required jobs
    # I.e. jobs depending on jobs that master-only job depend on
    _for_all_items(items, _save_requires_if_master)
    _for_all_items(items, _save_requires_if_master)
    return _do_filtering(items)
