def _savez(file, args, kwds, compress, allow_pickle=True, pickle_kwargs=None):
    # Import is postponed to here since zipfile depends on gzip, an optional
    # component of the so-called standard library.
    import zipfile

    if not hasattr(file, 'write'):
        file = os_fspath(file)
        if not file.endswith('.npz'):
            file = file + '.npz'

    namedict = kwds
    for i, val in enumerate(args):
        key = 'arr_%d' % i
        if key in namedict.keys():
            raise ValueError(
                "Cannot use un-named variables and keyword %s" % key)
        namedict[key] = val

    if compress:
        compression = zipfile.ZIP_DEFLATED
    else:
        compression = zipfile.ZIP_STORED

    zipf = zipfile_factory(file, mode="w", compression=compression)

    for key, val in namedict.items():
        fname = key + '.npy'
        val = np.asanyarray(val)
        # always force zip64, gh-10776
        with zipf.open(fname, 'w', force_zip64=True) as fid:
            format.write_array(fid, val,
                               allow_pickle=allow_pickle,
                               pickle_kwargs=pickle_kwargs)

    zipf.close()
