def fetch_kddcup99(subset=None, data_home=None, shuffle=False,
                   random_state=None,
                   percent10=True, download_if_missing=True):
    """Load and return the kddcup 99 dataset (classification).

    The KDD Cup '99 dataset was created by processing the tcpdump portions
    of the 1998 DARPA Intrusion Detection System (IDS) Evaluation dataset,
    created by MIT Lincoln Lab [1]. The artificial data was generated using
    a closed network and hand-injected attacks to produce a large number of
    different types of attack with normal activity in the background.
    As the initial goal was to produce a large training set for supervised
    learning algorithms, there is a large proportion (80.1%) of abnormal
    data which is unrealistic in real world, and inappropriate for unsupervised
    anomaly detection which aims at detecting 'abnormal' data, ie

    1) qualitatively different from normal data.

    2) in large minority among the observations.

    We thus transform the KDD Data set into two different data sets: SA and SF.

    - SA is obtained by simply selecting all the normal data, and a small
      proportion of abnormal data to gives an anomaly proportion of 1%.

    - SF is obtained as in [2]
      by simply picking up the data whose attribute logged_in is positive, thus
      focusing on the intrusion attack, which gives a proportion of 0.3% of
      attack.

    - http and smtp are two subsets of SF corresponding with third feature
      equal to 'http' (resp. to 'smtp')


    General KDD structure :

    ================      ==========================================
    Samples total         4898431
    Dimensionality        41
    Features              discrete (int) or continuous (float)
    Targets               str, 'normal.' or name of the anomaly type
    ================      ==========================================

    SA structure :

    ================      ==========================================
    Samples total         976158
    Dimensionality        41
    Features              discrete (int) or continuous (float)
    Targets               str, 'normal.' or name of the anomaly type
    ================      ==========================================

    SF structure :

    ================      ==========================================
    Samples total         699691
    Dimensionality        4
    Features              discrete (int) or continuous (float)
    Targets               str, 'normal.' or name of the anomaly type
    ================      ==========================================

    http structure :

    ================      ==========================================
    Samples total         619052
    Dimensionality        3
    Features              discrete (int) or continuous (float)
    Targets               str, 'normal.' or name of the anomaly type
    ================      ==========================================

    smtp structure :

    ================      ==========================================
    Samples total         95373
    Dimensionality        3
    Features              discrete (int) or continuous (float)
    Targets               str, 'normal.' or name of the anomaly type
    ================      ==========================================

    .. versionadded:: 0.18

    Parameters
    ----------
    subset : None, 'SA', 'SF', 'http', 'smtp'
        To return the corresponding classical subsets of kddcup 99.
        If None, return the entire kddcup 99 dataset.

    data_home : string, optional
        Specify another download and cache folder for the datasets. By default
        all scikit-learn data is stored in '~/scikit_learn_data' subfolders.
        .. versionadded:: 0.19

    shuffle : bool, default=False
        Whether to shuffle dataset.

    random_state : int, RandomState instance or None, optional (default=None)
        Random state for shuffling the dataset.
        If int, random_state is the seed used by the random number generator;
        If RandomState instance, random_state is the random number generator;
        If None, the random number generator is the RandomState instance used
        by `np.random`.

    percent10 : bool, default=True
        Whether to load only 10 percent of the data.

    download_if_missing : bool, default=True
        If False, raise a IOError if the data is not locally available
        instead of trying to download the data from the source site.

    Returns
    -------
    data : Bunch
        Dictionary-like object, the interesting attributes are:
        'data', the data to learn and 'target', the regression target for each
        sample.


    References
    ----------
    .. [1] Analysis and Results of the 1999 DARPA Off-Line Intrusion
           Detection Evaluation Richard Lippmann, Joshua W. Haines,
           David J. Fried, Jonathan Korba, Kumar Das

    .. [2] K. Yamanishi, J.-I. Takeuchi, G. Williams, and P. Milne. Online
           unsupervised outlier detection using finite mixtures with
           discounting learning algorithms. In Proceedings of the sixth
           ACM SIGKDD international conference on Knowledge discovery
           and data mining, pages 320-324. ACM Press, 2000.

    """
    data_home = get_data_home(data_home=data_home)
    kddcup99 = _fetch_brute_kddcup99(data_home=data_home, shuffle=shuffle,
                                     percent10=percent10,
                                     download_if_missing=download_if_missing)

    data = kddcup99.data
    target = kddcup99.target

    if subset == 'SA':
        s = target == b'normal.'
        t = np.logical_not(s)
        normal_samples = data[s, :]
        normal_targets = target[s]
        abnormal_samples = data[t, :]
        abnormal_targets = target[t]

        n_samples_abnormal = abnormal_samples.shape[0]
        # selected abnormal samples:
        random_state = check_random_state(random_state)
        r = random_state.randint(0, n_samples_abnormal, 3377)
        abnormal_samples = abnormal_samples[r]
        abnormal_targets = abnormal_targets[r]

        data = np.r_[normal_samples, abnormal_samples]
        target = np.r_[normal_targets, abnormal_targets]

    if subset == 'SF' or subset == 'http' or subset == 'smtp':
        # select all samples with positive logged_in attribute:
        s = data[:, 11] == 1
        data = np.c_[data[s, :11], data[s, 12:]]
        target = target[s]

        data[:, 0] = np.log((data[:, 0] + 0.1).astype(float))
        data[:, 4] = np.log((data[:, 4] + 0.1).astype(float))
        data[:, 5] = np.log((data[:, 5] + 0.1).astype(float))

        if subset == 'http':
            s = data[:, 2] == b'http'
            data = data[s]
            target = target[s]
            data = np.c_[data[:, 0], data[:, 4], data[:, 5]]

        if subset == 'smtp':
            s = data[:, 2] == b'smtp'
            data = data[s]
            target = target[s]
            data = np.c_[data[:, 0], data[:, 4], data[:, 5]]

        if subset == 'SF':
            data = np.c_[data[:, 0], data[:, 2], data[:, 4], data[:, 5]]

    return Bunch(data=data, target=target)
