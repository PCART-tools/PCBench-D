    def on_step_end(self, args: TrainingArguments, state: TrainerState, control: TrainerControl, **kwargs):
        # Log
        if state.global_step == 1 and args.logging_first_step:
            control.should_log = True
        if args.logging_steps > 0 and state.global_step % args.logging_steps == 0:
            control.should_log = True

        # Evaluate
        if args.evaluation_strategy == EvaluationStrategy.STEPS and state.global_step % args.eval_steps == 0:
            control.should_evaluate = True
            if args.load_best_model_at_end:
                control.should_save = True

        # Save
        if not args.load_best_model_at_end and args.save_steps > 0 and state.global_step % args.save_steps == 0:
            control.should_save = True

        # End training
        if state.global_step >= state.max_steps:
            control.should_training_stop = True

        return control
