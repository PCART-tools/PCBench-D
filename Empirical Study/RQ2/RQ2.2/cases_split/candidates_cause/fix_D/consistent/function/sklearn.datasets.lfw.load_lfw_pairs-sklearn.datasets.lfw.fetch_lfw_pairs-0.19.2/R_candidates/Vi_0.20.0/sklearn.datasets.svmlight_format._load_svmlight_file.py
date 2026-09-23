    def _load_svmlight_file(*args, **kwargs):
        raise NotImplementedError(
                'load_svmlight_file is currently not '
                'compatible with PyPy (see '
                'https://github.com/scikit-learn/scikit-learn/issues/11543 '
                'for the status updates).')
