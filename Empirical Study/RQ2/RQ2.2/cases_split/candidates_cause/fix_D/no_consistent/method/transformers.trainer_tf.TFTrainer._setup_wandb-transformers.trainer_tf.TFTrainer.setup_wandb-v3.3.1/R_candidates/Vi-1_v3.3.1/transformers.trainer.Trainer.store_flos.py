    def store_flos(self):
        # Storing the number of floating-point operations that went into the model
        if self.total_flos is not None:
            if self.args.local_rank != -1:
                total_flos = distributed_broadcast_scalars([self.total_flos]).sum().item()
            else:
                total_flos = self.total_flos
            if total_flos > 0:
                self.model.config.total_flos = total_flos
