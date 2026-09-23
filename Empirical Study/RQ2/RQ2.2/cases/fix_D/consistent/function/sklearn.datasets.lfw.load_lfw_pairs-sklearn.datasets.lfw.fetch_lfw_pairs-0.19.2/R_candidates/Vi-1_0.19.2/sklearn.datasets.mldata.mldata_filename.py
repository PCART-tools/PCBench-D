def mldata_filename(dataname):
    """Convert a raw name for a data set in a mldata.org filename.

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
