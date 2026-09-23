def teardown_module(module):
    from sklearn.utils.testing import uninstall_mldata_mock
    uninstall_mldata_mock()
