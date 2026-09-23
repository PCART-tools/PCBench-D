def dump_datasets(filename):
    base, ext = os.path.splitext(os.path.basename(filename))
    base += '_%s' % ext[1:]
    datadir = os.path.join(DATA_DIR, base)
    os.makedirs(datadir)
    datasets = parse_ipp_file(filename)
    for k, d in datasets.items():
        print(k, len(d))
        dfilename = os.path.join(datadir, k) + '.txt'
        dump_dataset(dfilename, d)
