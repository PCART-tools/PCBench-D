import torch
import inspect
from torch.ao.quantization.qconfig import QConfigDynamic

def main():
    activation = torch.nn.Identity
    weight = torch.nn.Identity
    qconfig_dynamic = QConfigDynamic(activation=activation, weight=weight)
    print("QConfigDynamic:", qconfig_dynamic)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(QConfigDynamic))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()