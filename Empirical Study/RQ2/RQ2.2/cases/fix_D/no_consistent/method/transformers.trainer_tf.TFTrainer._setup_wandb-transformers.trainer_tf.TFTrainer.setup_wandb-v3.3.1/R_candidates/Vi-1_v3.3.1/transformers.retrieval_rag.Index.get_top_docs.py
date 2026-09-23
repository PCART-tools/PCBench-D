    def get_top_docs(self, question_hidden_states: np.ndarray, n_docs=5) -> Tuple[np.ndarray, np.ndarray]:
        """
        For each query in the batch, retrieves ``n_docs`` documents.

        Args:
            question_hidden_states (:obj:`np.ndarray` of shape :obj:`(batch_size, vector_size):
                An array of query vectors.
            n_docs (:obj:`int`):
                The number of docs retrieved per query.

        Returns:
            :obj:`np.ndarray` of shape :obj:`(batch_size, n_docs)`: A tensor of indices of retrieved documents.
            :obj:`np.ndarray` of shape :obj:`(batch_size, vector_size)`: A tensor of vector representations of retrieved documents.
        """
        raise NotImplementedError
