def changed_files() -> Optional[List[str]]:
    changed_files: Optional[List[str]] = None
    try:
        changed_files = sorted(find_changed_files())
    except Exception:
        # If the git commands failed for some reason, bail out and use the whole list
        print(
            "Could not query git for changed files, falling back to testing all files instead",
            file=sys.stderr,
        )
        return None

    return changed_files
