def collate_into_packed_sequence_batch_first(batch):
    data = torch.stack([sample[0] for sample in batch], 0)
    b, t = data.size()
    lengths = torch.randint(1, t, size=(b,), dtype=torch.int64)
    return torch.nn.utils.rnn.pack_padded_sequence(data, lengths, batch_first=True, enforce_sorted=False)
