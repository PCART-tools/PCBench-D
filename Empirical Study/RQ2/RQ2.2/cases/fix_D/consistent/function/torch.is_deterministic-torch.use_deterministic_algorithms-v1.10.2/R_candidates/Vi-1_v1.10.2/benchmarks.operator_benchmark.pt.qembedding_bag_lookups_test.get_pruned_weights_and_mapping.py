def get_pruned_weights_and_mapping(q_weights):
    indicator = torch.from_numpy(np.random.uniform(
        low=-1.0, high=1.0, size=[q_weights.shape[0]]).astype(np.float32))

    q_pruned_weights, compressed_indices_mapping = torch.ops.fb.embedding_bag_rowwise_prune(
        q_weights, indicator, 0.01, torch.int32)

    return q_pruned_weights, compressed_indices_mapping
