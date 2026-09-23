def get_label(line):
    m = label_re.match(line)
    if m:
        return m.group(1)
