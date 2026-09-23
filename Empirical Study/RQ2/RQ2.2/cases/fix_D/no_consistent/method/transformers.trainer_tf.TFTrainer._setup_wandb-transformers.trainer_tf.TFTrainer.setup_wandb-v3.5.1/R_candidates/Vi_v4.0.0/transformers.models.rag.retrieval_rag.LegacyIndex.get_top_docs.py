    def get_top_docs(self, question_hidden_states: np.ndarray, n_docs=5) -> Tuple[np.ndarray, np.ndarray]:
        aux_dim = np.zeros(len(question_hidden_states), dtype="float32").reshape(-1, 1)
        query_nhsw_vectors = np.hstack((question_hidden_states, aux_dim))
        _, docs_ids = self.index.search(query_nhsw_vectors, n_docs)
        vectors = [[self.index.reconstruct(int(doc_id))[:-1] for doc_id in doc_ids] for doc_ids in docs_ids]
        ids = [[int(self.index_id_to_db_id[doc_id]) for doc_id in doc_ids] for doc_ids in docs_ids]
        return np.array(ids), np.array(vectors)
