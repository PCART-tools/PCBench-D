    def get_feature_names(self):
        """Get feature names from all transformers.

        Returns
        -------
        feature_names : list of strings
            Names of the features produced by transform.
        """
        check_is_fitted(self)
        feature_names = []
        for name, trans, column, _ in self._iter(fitted=True):
            if trans == 'drop' or (
                    hasattr(column, '__len__') and not len(column)):
                continue
            if trans == 'passthrough':
                if hasattr(self, '_df_columns'):
                    if ((not isinstance(column, slice))
                            and all(isinstance(col, str) for col in column)):
                        feature_names.extend(column)
                    else:
                        feature_names.extend(self._df_columns[column])
                else:
                    indices = np.arange(self._n_features)
                    feature_names.extend(['x%d' % i for i in indices[column]])
                continue
            if not hasattr(trans, 'get_feature_names'):
                raise AttributeError("Transformer %s (type %s) does not "
                                     "provide get_feature_names."
                                     % (str(name), type(trans).__name__))
            feature_names.extend([name + "__" + f for f in
                                  trans.get_feature_names()])
        return feature_names
