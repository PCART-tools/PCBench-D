    def __getstate__(self):
        state = self.__dict__.copy()
        # the C object _contour_generator cannot currently be pickled. This
        # isn't a big issue as it is not actually used once the contour has
        # been calculated.
        state['_contour_generator'] = None
        return state
