def _recommend_auto_balance(message: str) -> str:
    """Expands a message with recommendation to :mod:`torchpipe.balance`."""
    return f"""{message}

If your model is still under development, its optimal balance would change
frequently. In this case, we highly recommend 'torch.distributed.pipeline.sync.balance' for
naive automatic balancing:

  from torch.distributed.pipeline.sync import Pipe
  from torch.distributed.pipeline.sync.balance import balance_by_time

  partitions = torch.cuda.device_count()
  sample = torch.empty(...)
  balance = balance_by_time(partitions, model, sample)

  model = Pipe(model, balance, ...)
"""
