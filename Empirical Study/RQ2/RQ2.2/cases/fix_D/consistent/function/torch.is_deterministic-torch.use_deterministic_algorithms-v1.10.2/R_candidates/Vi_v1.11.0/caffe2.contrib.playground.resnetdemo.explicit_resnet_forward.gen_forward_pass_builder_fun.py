def gen_forward_pass_builder_fun(self, model, dataset, is_train):
    split = 'train' if is_train else 'test'
    opts = self.opts

    def model_creator(model, loss_scale):
        model, softmax, loss = resnet_imagenet_create_model(
            model=model,
            data='data',
            labels='label',
            split=split,
            opts=opts,
            dataset=dataset,
        )
        return [loss]
    return model_creator
