def _fetch_brute_kddcup99(data_home=None,
                          download_if_missing=True, random_state=None,
                          shuffle=False, percent10=True):

    """Load the kddcup99 dataset, downloading it if necessary.

    Parameters
    ----------
    data_home : string, optional
        Specify another download and cache folder for the datasets. By default
        all scikit-learn data is stored in '~/scikit_learn_data' subfolders.

    download_if_missing : boolean, default=True
        If False, raise a IOError if the data is not locally available
        instead of trying to download the data from the source site.

    random_state : int, RandomState instance or None, optional (default=None)
        Random state for shuffling the dataset.
        If int, random_state is the seed used by the random number generator;
        If RandomState instance, random_state is the random number generator;
        If None, the random number generator is the RandomState instance used
        by `np.random`.

    shuffle : bool, default=False
        Whether to shuffle dataset.

    percent10 : bool, default=True
        Whether to load only 10 percent of the data.

    Returns
    -------
    dataset : dict-like object with the following attributes:
        dataset.data : numpy array of shape (494021, 41)
            Each row corresponds to the 41 features in the dataset.
        dataset.target : numpy array of shape (494021,)
            Each value corresponds to one of the 21 attack types or to the
            label 'normal.'.
        dataset.DESCR : string
            Description of the kddcup99 dataset.

    """

    data_home = get_data_home(data_home=data_home)
    if sys.version_info[0] == 3:
        # The zlib compression format use by joblib is not compatible when
        # switching from Python 2 to Python 3, let us use a separate folder
        # under Python 3:
        dir_suffix = "-py3"
    else:
        # Backward compat for Python 2 users
        dir_suffix = ""

    if percent10:
        kddcup_dir = join(data_home, "kddcup99_10" + dir_suffix)
        archive = ARCHIVE_10_PERCENT
    else:
        kddcup_dir = join(data_home, "kddcup99" + dir_suffix)
        archive = ARCHIVE

    samples_path = join(kddcup_dir, "samples")
    targets_path = join(kddcup_dir, "targets")
    available = exists(samples_path)

    if download_if_missing and not available:
        _mkdirp(kddcup_dir)
        logger.info("Downloading %s" % archive.url)
        _fetch_remote(archive, dirname=kddcup_dir)
        dt = [('duration', int),
              ('protocol_type', 'S4'),
              ('service', 'S11'),
              ('flag', 'S6'),
              ('src_bytes', int),
              ('dst_bytes', int),
              ('land', int),
              ('wrong_fragment', int),
              ('urgent', int),
              ('hot', int),
              ('num_failed_logins', int),
              ('logged_in', int),
              ('num_compromised', int),
              ('root_shell', int),
              ('su_attempted', int),
              ('num_root', int),
              ('num_file_creations', int),
              ('num_shells', int),
              ('num_access_files', int),
              ('num_outbound_cmds', int),
              ('is_host_login', int),
              ('is_guest_login', int),
              ('count', int),
              ('srv_count', int),
              ('serror_rate', float),
              ('srv_serror_rate', float),
              ('rerror_rate', float),
              ('srv_rerror_rate', float),
              ('same_srv_rate', float),
              ('diff_srv_rate', float),
              ('srv_diff_host_rate', float),
              ('dst_host_count', int),
              ('dst_host_srv_count', int),
              ('dst_host_same_srv_rate', float),
              ('dst_host_diff_srv_rate', float),
              ('dst_host_same_src_port_rate', float),
              ('dst_host_srv_diff_host_rate', float),
              ('dst_host_serror_rate', float),
              ('dst_host_srv_serror_rate', float),
              ('dst_host_rerror_rate', float),
              ('dst_host_srv_rerror_rate', float),
              ('labels', 'S16')]
        DT = np.dtype(dt)
        logger.debug("extracting archive")
        archive_path = join(kddcup_dir, archive.filename)
        file_ = GzipFile(filename=archive_path, mode='r')
        Xy = []
        for line in file_.readlines():
            if six.PY3:
                line = line.decode()
            Xy.append(line.replace('\n', '').split(','))
        file_.close()
        logger.debug('extraction done')
        os.remove(archive_path)

        Xy = np.asarray(Xy, dtype=object)
        for j in range(42):
            Xy[:, j] = Xy[:, j].astype(DT[j])

        X = Xy[:, :-1]
        y = Xy[:, -1]
        # XXX bug when compress!=0:
        # (error: 'Incorrect data length while decompressing[...] the file
        #  could be corrupted.')

        joblib.dump(X, samples_path, compress=0)
        joblib.dump(y, targets_path, compress=0)
    elif not available:
        if not download_if_missing:
            raise IOError("Data not found and `download_if_missing` is False")

    try:
        X, y
    except NameError:
        X = joblib.load(samples_path)
        y = joblib.load(targets_path)

    if shuffle:
        X, y = shuffle_method(X, y, random_state=random_state)

    return Bunch(data=X, target=y, DESCR=__doc__)
