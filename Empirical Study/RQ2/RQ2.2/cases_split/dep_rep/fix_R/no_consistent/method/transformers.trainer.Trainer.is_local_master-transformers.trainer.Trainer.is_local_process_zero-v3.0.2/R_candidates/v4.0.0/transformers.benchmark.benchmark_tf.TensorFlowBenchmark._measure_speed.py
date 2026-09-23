    def _measure_speed(self, func) -> float:
        with self.args.strategy.scope():
            try:
                if self.args.is_tpu or self.args.use_xla:
                    # run additional 10 times to stabilize compilation for tpu
                    logger.info("Do inference on TPU. Running model 5 times to stabilize compilation")
                    timeit.repeat(func, repeat=1, number=5)

                # as written in https://docs.python.org/2/library/timeit.html#timeit.Timer.repeat, min should be taken rather than the average
                runtimes = timeit.repeat(
                    func,
                    repeat=self.args.repeat,
                    number=10,
                )

                return min(runtimes) / 10.0
            except ResourceExhaustedError as e:
                self.print_fn("Doesn't fit on GPU. {}".format(e))
