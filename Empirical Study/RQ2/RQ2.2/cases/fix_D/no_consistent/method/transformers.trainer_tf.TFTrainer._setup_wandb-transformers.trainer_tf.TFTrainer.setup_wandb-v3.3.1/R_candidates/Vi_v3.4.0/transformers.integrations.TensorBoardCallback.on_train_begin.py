    def on_train_begin(self, args, state, control, **kwargs):
        if self.tb_writer is not None:
            self.tb_writer.add_text("args", args.to_json_string())
            self.tb_writer.add_hparams(args.to_sanitized_dict(), metric_dict={})
