def collate_into_packed_sequence(batch):
    data = torch.stack([sample[0] for sample in batch], 1)
    t, b = data.size()
    lengths = torch.randint(1, t, size=(b,), dtype=torch.int64)
    return torch.nn.utils.rnn.pack_padded_sequence(data, lengths, enforce_sorted=False)
