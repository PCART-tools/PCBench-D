def parse_ipp_file(filename):
    print(filename)
    a = open(filename, 'r')
    lines = a.readlines()
    data = {}
    i = 0
    while (i < len(lines)):
        line = lines[i]
        m = HEADER_REGEX.search(line)
        if m:
            d = int(m.group(1))
            n = int(m.group(2))
            print("d = {0}, n = {1}".format(d, n))
            cdata = []
            i += 1
            line = lines[i]
            # Skip comments
            while CXX_COMMENT.match(line):
                i += 1
                line = lines[i]
            while DATA_REGEX.match(line):
                cdata.append(_raw_data(line))
                i += 1
                line = lines[i]
                # Skip comments
                while CXX_COMMENT.match(line):
                    i += 1
                    line = lines[i]
            if not len(cdata) == n:
                raise ValueError("parsed data: %d, expected %d" % (len(cdata), n))
            data[m.group(3)] = cdata
        else:
            i += 1

    return data
