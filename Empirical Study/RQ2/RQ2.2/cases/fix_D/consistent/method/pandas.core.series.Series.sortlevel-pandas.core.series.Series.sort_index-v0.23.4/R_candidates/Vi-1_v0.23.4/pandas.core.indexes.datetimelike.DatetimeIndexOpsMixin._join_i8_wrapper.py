    @staticmethod
    def _join_i8_wrapper(joinf, dtype, with_indexers=True):
        """ create the join wrapper methods """

        @staticmethod
        def wrapper(left, right):
            if isinstance(left, (np.ndarray, ABCIndex, ABCSeries)):
                left = left.view('i8')
            if isinstance(right, (np.ndarray, ABCIndex, ABCSeries)):
                right = right.view('i8')
            results = joinf(left, right)
            if with_indexers:
                join_index, left_indexer, right_indexer = results
                join_index = join_index.view(dtype)
                return join_index, left_indexer, right_indexer
            return results

        return wrapper
