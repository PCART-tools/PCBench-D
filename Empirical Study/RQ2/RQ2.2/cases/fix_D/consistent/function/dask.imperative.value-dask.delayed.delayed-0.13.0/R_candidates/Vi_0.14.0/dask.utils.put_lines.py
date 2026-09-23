def put_lines(buf, lines):
    if any(not isinstance(x, unicode) for x in lines):
        lines = [unicode(x) for x in lines]
    buf.write('\n'.join(lines))
