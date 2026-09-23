def train(lm_dataloader, model, criterion, optimizer, vocab_size, args):
    model.train()

    vocab_size = 10000
    total_loss = 0.0
    start_time = time.time()
    word_counter = 0

    optimizer = optimizer(model)

    def get_first_device(model):
        if model.devices:
            return model.devices[0]
        else:
            return torch.cuda.current_device()

    def get_last_device(model):
        if model.devices:
            return model.devices[-1]
        else:
            return torch.cuda.current_device()


    print('Number of parameters for model: {}'.format(sum(p.numel() for p in model.parameters())))
    for i, batch in enumerate(lm_dataloader):
        bi = batch["input"]
        if args.max_batch and i > args.max_batch:
            break
        optimizer.zero_grad()
        try:
            tmp = batch["input"].to(get_first_device(model))
            output = model(tmp).local_value()
        except Exception as e:
            raise RuntimeError(f"training failed on {torch.distributed.get_rank()}") from e

        target = batch["target"].to(get_last_device(model))
        output = output.to(target.device)

        loss = criterion(output.view(-1, vocab_size), target.view(-1))
        loss.backward()
        del target
        del output

        torch.nn.utils.clip_grad_value_(model.parameters(), 0.05)
        optimizer.step()

        total_loss += loss.item()
        log_interval = 1
        word_counter += batch["ntokens"]
        if i % log_interval == 0 and i > 0:
            cur_loss = total_loss / log_interval
            elapsed = time.time() - start_time
            print(
                "| batch {:5d} | wps {:5.2f} | loss {:5.2f} | ppl {:8.2f}".format(
                    i, word_counter / elapsed, cur_loss, math.exp(cur_loss)
                )
            )
            word_counter = 0
            total_loss = 0
            start_time = time.time()

    print('Peak memory usage for GPUs: ', end='')
    for i in range(len(model.devices)):
        print("cuda:{}: {}, ".format(
            i,
            sizeof_fmt(torch.cuda.memory_stats(i)["allocated_bytes.all.peak"])), end='')
    print()
