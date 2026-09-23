def summary(analysis: List[SuiteDiff]) -> str:
    removed_tests: DefaultDict[str, List[CaseDiff]] = defaultdict(list)
    modified_tests: DefaultDict[str, List[CaseDiff]] = defaultdict(list)
    added_tests: DefaultDict[str, List[CaseDiff]] = defaultdict(list)

    for diff in analysis:
        # the use of 'margin' here is not the most elegant
        name = diff['name']
        margin = diff['margin']
        cases = diff['cases']
        if margin == '-':
            removed_tests[name] += cases
        elif margin == '+':
            added_tests[name] += cases
        else:
            removed = list(filter(lambda c: c['margin'] == '-', cases))
            added = list(filter(lambda c: c['margin'] == '+', cases))
            modified = list(filter(lambda c: c['margin'] == '!', cases))
            if removed:
                removed_tests[name] += removed
            if added:
                added_tests[name] += added
            if modified:
                modified_tests[name] += modified

    return unlines([
        summary_line('Removed ', removed_tests),
        summary_line('Modified', modified_tests),
        summary_line('Added   ', added_tests),
    ])
