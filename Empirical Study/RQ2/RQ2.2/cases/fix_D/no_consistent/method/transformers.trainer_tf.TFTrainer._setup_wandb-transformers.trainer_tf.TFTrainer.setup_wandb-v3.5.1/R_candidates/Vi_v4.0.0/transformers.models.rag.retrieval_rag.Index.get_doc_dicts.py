    def get_doc_dicts(self, doc_ids: np.ndarray) -> List[dict]:
        """
        Returns a list of dictionaries, containing titles and text of the retrieved documents.

        Args:
            doc_ids (:obj:`np.ndarray` of shape :obj:`(batch_size, n_docs)`):
                A tensor of document indices.
        """
        raise NotImplementedError
