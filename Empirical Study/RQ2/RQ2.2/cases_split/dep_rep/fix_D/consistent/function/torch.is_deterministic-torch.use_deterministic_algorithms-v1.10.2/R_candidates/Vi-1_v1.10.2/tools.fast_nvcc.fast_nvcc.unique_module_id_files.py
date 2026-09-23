def unique_module_id_files(commands: List[str]) -> List[str]:
    """
    Give each command its own .module_id filename instead of sharing.
    """
    module_id = None
    uniqueified = []
    for i, line in enumerate(commands):
        arr = []

        def uniqueify(s: Match[str]) -> str:
            filename = re.sub(r'\-(\d+)', r'-\1-' + str(i), s.group(0))
            arr.append(filename)
            return filename

        line = re.sub(re_tmp + r'.module_id', uniqueify, line)
        line = re.sub(r'\s*\-\-gen\_module\_id\_file\s*', ' ', line)
        if arr:
            filename, = arr
            if not module_id:
                module_id = module_id_contents(shlex.split(line))
            uniqueified.append(f"echo -n '{module_id}' > '{filename}'")
        uniqueified.append(line)
    return uniqueified
