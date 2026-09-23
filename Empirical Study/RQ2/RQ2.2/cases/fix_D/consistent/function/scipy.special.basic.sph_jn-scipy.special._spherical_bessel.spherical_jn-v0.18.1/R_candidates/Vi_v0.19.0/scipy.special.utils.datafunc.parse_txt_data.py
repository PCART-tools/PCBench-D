def parse_txt_data(filename):
    f = open(filename)
    try:
        reader = csv.reader(f, delimiter=',')
        data = []
        for row in reader:
            data.append(list(map(float, row)))
        nc = len(data[0])
        for i in data:
            if not nc == len(i):
                raise ValueError(i)
        ## guess number of columns/rows
        #row0 = f.readline()
        #nc = len(row0.split(',')) - 1
        #nlines = len(f.readlines()) + 1
        #f.seek(0)
        #data = np.fromfile(f, sep=',')
        #if not data.size == nc * nlines:
        #    raise ValueError("Inconsistency between array (%d items) and "
        #                     "guessed data size %dx%d" % (data.size, nlines, nc))
        #data = data.reshape((nlines, nc))
        #return data
    finally:
        f.close()

    return np.array(data)
