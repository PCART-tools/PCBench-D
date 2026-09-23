def setup_module(module):
    # setup mock urllib2 module to avoid downloading from mldata.org
    from sklearn.utils.testing import install_mldata_mock
    install_mldata_mock({
        'iris': {
            'data': np.empty((150, 4)),
            'label': np.empty(150),
        },
        'datasets-uci-iris': {
            'double0': np.empty((150, 4)),
            'class': np.empty((150,)),
        },
        'leukemia': {
            'data': np.empty((72, 7129)),
        },
    })
