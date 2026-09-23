def make_model_and_data(args, device):
    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    vocab_size = 10000
    model, criterion, optimizer = make_model(args, device, vocab_size)
    lm_dataset = BenchmarkLMDataset()
    lm_dataloader = DataLoader(
        lm_dataset, batch_size=args.batch_size, shuffle=True, num_workers=0, collate_fn=collate_sentences_lm
    )
    return {
        "model": model,
        "criterion": criterion,
        "optimizer": optimizer,
        "data": lm_dataloader,
        "vocab_size": vocab_size,
    }
