    def on_init_end(self, args, state, control, **kwargs):
        if self.tb_writer is None and state.is_world_process_zero:
            self.tb_writer = SummaryWriter(log_dir=args.logging_dir)
