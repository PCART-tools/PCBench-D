    def is_local_master(self) -> bool:
        """
        Whether or not this process is the local (e.g., on one machine if training in a distributed fashion on
        several machines) main process.

        .. warning::

            This method is deprecated, use :meth:`~transformers.Trainer.is_local_process_zero` instead.
        """
        warnings.warn("This method is deprecated, use `Trainer.is_local_process_zero()` instead.", FutureWarning)
        return self.is_local_process_zero()
