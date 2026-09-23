def mpl_style_cb(key):
    import sys
    from pandas.tools.plotting import mpl_stylesheet
    global style_backup

    val = cf.get_option(key)

    if 'matplotlib' not in sys.modules.keys():
        if not(val):  # starting up, we get reset to None
            return val
        raise Exception("matplotlib has not been imported. aborting")

    import matplotlib.pyplot as plt

    if val == 'default':
        style_backup = dict([(k, plt.rcParams[k]) for k in mpl_stylesheet])
        plt.rcParams.update(mpl_stylesheet)
    elif not val:
        if style_backup:
            plt.rcParams.update(style_backup)

    return val
