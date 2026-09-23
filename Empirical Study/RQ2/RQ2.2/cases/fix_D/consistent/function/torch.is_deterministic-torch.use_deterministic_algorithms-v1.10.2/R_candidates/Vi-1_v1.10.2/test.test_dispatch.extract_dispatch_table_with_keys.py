def extract_dispatch_table_with_keys(table, dispatch_keys):
    extracted = ''
    table_entries = table.split('\n')
    regex = re.compile(r"registered at .*FallbackKernel\.cpp.*(\[)")
    for k in dispatch_keys:
        for t in table_entries:
            if t.startswith(k):
                # mask out file:line info for in-tree backend fallback
                entry = regex.sub('registered in pytorch framework [', t)
                extracted += (entry + '\n')
    return extracted
