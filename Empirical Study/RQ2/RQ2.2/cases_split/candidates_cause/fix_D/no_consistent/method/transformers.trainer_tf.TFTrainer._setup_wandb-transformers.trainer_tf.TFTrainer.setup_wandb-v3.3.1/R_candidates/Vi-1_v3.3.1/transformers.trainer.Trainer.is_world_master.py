    def is_world_master(self) -> bool:
        """
        Whether or not this process is the global main process (when training in a distributed fashion on
        several machines, this is only going to be :obj:`True` for one process).

        .. warning::

            This method is deprecated, use :meth:`~transformers.Trainer.is_world_process_zero` instead.
        """
        warnings.warn("This method is deprecated, use `Trainer.is_world_process_zero()` instead.", FutureWarning)
        return self.is_world_process_zero()
