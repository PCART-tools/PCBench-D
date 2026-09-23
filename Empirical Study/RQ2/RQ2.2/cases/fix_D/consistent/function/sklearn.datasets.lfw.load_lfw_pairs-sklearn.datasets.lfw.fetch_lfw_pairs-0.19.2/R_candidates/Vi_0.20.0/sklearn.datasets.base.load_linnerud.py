def load_linnerud(return_X_y=False):
    """Load and return the linnerud dataset (multivariate regression).

    ==============    ============================
    Samples total     20
    Dimensionality    3 (for both data and target)
    Features          integer
    Targets           integer
    ==============    ============================

    Read more in the :ref:`User Guide <linnerrud_dataset>`.

    Parameters
    ----------
    return_X_y : boolean, default=False.
        If True, returns ``(data, target)`` instead of a Bunch object.
        See below for more information about the `data` and `target` object.

        .. versionadded:: 0.18

    Returns
    -------
    data : Bunch
        Dictionary-like object, the interesting attributes are: 'data' and
        'targets', the two multivariate datasets, with 'data' corresponding to
        the exercise and 'targets' corresponding to the physiological
        measurements, as well as 'feature_names' and 'target_names'.
        In addition, you will also have access to 'data_filename',
        the physical location of linnerud data csv dataset, and
        'target_filename', the physical location of
        linnerud targets csv datataset (added in version `0.20`).

    (data, target) : tuple if ``return_X_y`` is True

        .. versionadded:: 0.18
    """
    base_dir = join(dirname(__file__), 'data/')
    data_filename = join(base_dir, 'linnerud_exercise.csv')
    target_filename = join(base_dir, 'linnerud_physiological.csv')

    # Read data
    data_exercise = np.loadtxt(data_filename, skiprows=1)
    data_physiological = np.loadtxt(target_filename, skiprows=1)

    # Read header
    with open(data_filename) as f:
        header_exercise = f.readline().split()
    with open(target_filename) as f:
        header_physiological = f.readline().split()

    with open(dirname(__file__) + '/descr/linnerud.rst') as f:
        descr = f.read()

    if return_X_y:
        return data_exercise, data_physiological

    return Bunch(data=data_exercise, feature_names=header_exercise,
                 target=data_physiological,
                 target_names=header_physiological,
                 DESCR=descr,
                 data_filename=data_filename,
                 target_filename=target_filename)
