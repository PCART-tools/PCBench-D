def collate_sentences_lm(samples):

    if len(samples) == 0:
        return {}

    id = torch.LongTensor([s["id"] for s in samples])
    src_tokens = torch.stack([s["source"] for s in samples], 0)
    tgt_tokens = torch.stack([s["target"] for s in samples], 0)
    ntokens = len(samples) * len(samples[0]["target"])
    src_lengths = torch.LongTensor([len(samples[0]["source"])] * len(samples))

    batch = {
        "id": id,
        "nsentences": len(samples),
        "ntokens": ntokens,
        "input": src_tokens,
        "target": tgt_tokens,
    }
    return batch
