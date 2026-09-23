    @staticmethod
    def _get_step_inputs(batch, nb_instances):

        features, labels = batch

        if isinstance(labels, PerReplica):
            # need to make a `PerReplica` objects for ``nb_instances``
            nb_instances = PerReplica([nb_instances] * len(labels.values))

        step_inputs = (features, labels, nb_instances)

        return step_inputs
