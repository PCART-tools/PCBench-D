        def hash_object_array(x, hash_key, encoding):
            return np.array([hash(i) for i in x], dtype=np.uint64)
