def main():
    model = torchvision.models.mobilenet_v2(pretrained=True)
    model.eval()
    example = torch.rand(1, 3, 224, 224)
    model = torch.jit.trace(model, example)
    compile_spec = mobilenetv2_spec()
    mlmodel = torch._C._jit_to_backend("coreml", model, compile_spec)
    print(mlmodel._c._get_method("forward").graph)
    mlmodel._save_for_lite_interpreter("../models/model_coreml.ptl")
