    def run(self):
        result_dict = {model_name: {} for model_name in self.args.model_names}
        inference_result_time = copy.deepcopy(result_dict)
        inference_result_memory = copy.deepcopy(result_dict)
        train_result_time = copy.deepcopy(result_dict)
        train_result_memory = copy.deepcopy(result_dict)

        for c, model_name in enumerate(self.args.model_names):
            self.print_fn(f"{c + 1} / {len(self.args.model_names)}")

            model_dict = {
                "bs": self.args.batch_sizes,
                "ss": self.args.sequence_lengths,
                "result": {i: {} for i in self.args.batch_sizes},
            }
            inference_result_time[model_name] = copy.deepcopy(model_dict)
            inference_result_memory[model_name] = copy.deepcopy(model_dict)
            train_result_time[model_name] = copy.deepcopy(model_dict)
            train_result_memory[model_name] = copy.deepcopy(model_dict)

            inference_summary = train_summary = None

            for batch_size in self.args.batch_sizes:
                for sequence_length in self.args.sequence_lengths:
                    if self.args.inference:
                        if self.args.memory:
                            memory, inference_summary = self.inference_memory(model_name, batch_size, sequence_length)
                            inference_result_memory[model_name]["result"][batch_size][sequence_length] = memory
                        if self.args.speed:
                            time = self.inference_speed(model_name, batch_size, sequence_length)
                            inference_result_time[model_name]["result"][batch_size][sequence_length] = time

                    if self.args.training:
                        if self.args.memory:
                            memory, train_summary = self.train_memory(model_name, batch_size, sequence_length)
                            train_result_memory[model_name]["result"][batch_size][sequence_length] = memory
                        if self.args.speed:
                            time = self.train_speed(model_name, batch_size, sequence_length)
                            train_result_time[model_name]["result"][batch_size][sequence_length] = time

        if self.args.inference:
            if self.args.speed:
                self.print_fn("\n" + 20 * "=" + ("INFERENCE - SPEED - RESULT").center(40) + 20 * "=")
                self.print_results(inference_result_time, type_label="Time in s")
                self.save_to_csv(inference_result_time, self.args.inference_time_csv_file)
                if self.args.is_tpu:
                    self.print_fn(
                        "TPU was used for inference. Note that the time after compilation stabilized (after ~10 inferences model.forward(..) calls) was measured."
                    )

            if self.args.memory:
                self.print_fn("\n" + 20 * "=" + ("INFERENCE - MEMORY - RESULT").center(40) + 20 * "=")
                self.print_results(inference_result_memory, type_label="Memory in MB")
                self.save_to_csv(inference_result_memory, self.args.inference_memory_csv_file)

            if self.args.trace_memory_line_by_line:
                self.print_fn("\n" + 20 * "=" + ("INFERENCE - MEMOMRY - LINE BY LINE - SUMMARY").center(40) + 20 * "=")
                self.print_memory_trace_statistics(inference_summary)

        if self.args.training:
            if self.args.speed:
                self.print_fn("\n" + 20 * "=" + ("TRAIN - SPEED - RESULTS").center(40) + 20 * "=")
                self.print_results(train_result_time, "Time in s")
                self.save_to_csv(train_result_time, self.args.train_time_csv_file)
                if self.args.is_tpu:
                    self.print_fn(
                        "TPU was used for training. Note that the time after compilation stabilized (after ~10 train loss=model.forward(...) + loss.backward() calls) was measured."
                    )

            if self.args.memory:
                self.print_fn("\n" + 20 * "=" + ("TRAIN - MEMORY - RESULTS").center(40) + 20 * "=")
                self.print_results(train_result_memory, type_label="Memory in MB")
                self.save_to_csv(train_result_memory, self.args.train_memory_csv_file)

            if self.args.trace_memory_line_by_line:
                self.print_fn("\n" + 20 * "=" + ("TRAIN - MEMOMRY - LINE BY LINE - SUMMARY").center(40) + 20 * "=")
                self.print_memory_trace_statistics(train_summary)

        if self.args.env_print:
            self.print_fn("\n" + 20 * "=" + ("ENVIRONMENT INFORMATION").center(40) + 20 * "=")
            self.print_fn(
                "\n".join(["- {}: {}".format(prop, val) for prop, val in self.environment_info.items()]) + "\n"
            )

        if self.args.save_to_csv:
            with open(self.args.env_info_csv_file, mode="w", newline="") as csv_file:
                writer = csv.writer(csv_file)
                for key, value in self.environment_info.items():
                    writer.writerow([key, value])

        return BenchmarkOutput(
            inference_result_time,
            inference_result_memory,
            train_result_time,
            train_result_memory,
            inference_summary,
            train_summary,
        )
