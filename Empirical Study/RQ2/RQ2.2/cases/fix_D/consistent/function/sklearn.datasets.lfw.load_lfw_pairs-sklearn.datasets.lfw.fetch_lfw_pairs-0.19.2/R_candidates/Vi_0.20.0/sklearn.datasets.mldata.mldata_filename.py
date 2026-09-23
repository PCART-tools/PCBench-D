@deprecated('mldata_filename was deprecated in version 0.20 and will be '
            'removed in version 0.22')
def mldata_filename(dataname):
    """Convert a raw name for a data set in a mldata.org filename.

    .. deprecated:: 0.20
        Will be removed in version 0.22

    Parameters
    ----------
    dataname : str
        Name of dataset

    Returns
    -------
    fname : str
        The converted dataname.
    """
    dataname = dataname.lower().replace(' ', '-')
    return re.sub(r'[().]', '', dataname)
