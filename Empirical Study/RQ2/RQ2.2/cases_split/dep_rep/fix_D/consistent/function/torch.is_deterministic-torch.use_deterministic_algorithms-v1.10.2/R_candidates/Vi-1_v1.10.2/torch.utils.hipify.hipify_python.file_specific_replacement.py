def file_specific_replacement(filepath, search_string, replace_string, strict=False):
    with openf(filepath, "r+") as f:
        contents = f.read()
        if strict:
            contents = re.sub(r'\b({0})\b'.format(re.escape(search_string)), lambda x: replace_string, contents)
        else:
            contents = contents.replace(search_string, replace_string)
        f.seek(0)
        f.write(contents)
        f.truncate()
