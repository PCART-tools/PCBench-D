import inspect
from sklearn.datasets import load_lfw_pairs

def main():
    # 尝试加载 'test' 子集，避免 reshape 报错
    data = load_lfw_pairs(
        subset='test',
        data_home='/media/he/Rbench/PCBench-D/scikit-learn/sklearn.datasets.lfw.load_lfw_pairs@0.16.1'
    )
    print("LFW pairs data keys:", data.keys())

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(load_lfw_pairs))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
