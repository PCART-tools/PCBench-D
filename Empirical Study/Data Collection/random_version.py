import random

random.seed(2025)

def randomFiveVersion(Total):
    TempList=[]
    for i in range(5):
        TempVersion=-1
        while(True):        #保证返回的五个版本没有重复的
            TempVersion=random.randint(1,Total)
            if TempVersion not in TempList:
                break
        TempList.append(TempVersion)

    return TempList

if __name__=="__main__":
    #request
    RequestTotal=155
    print('request:\t',randomFiveVersion(RequestTotal))

    #numpy
    NumpyTotal=110
    print('numpy:\t\t',randomFiveVersion(NumpyTotal))

    #pandas
    PandasTotal=97
    print('pandas:\t\t',randomFiveVersion(PandasTotal))

    #click
    ClickTotal=42
    print('click:\t\t',randomFiveVersion(ClickTotal))

    #flask
    FlaskTotal=59
    print('flask:\t\t',randomFiveVersion(FlaskTotal))

    #pydantic
    PydanticTotal=132
    print('pydantic:\t',randomFiveVersion(PydanticTotal))

    #scipy
    ScipyTotal=72
    print('scipy:\t\t',randomFiveVersion(ScipyTotal))

    #pillow
    PillowTotal=62
    print('pillow:\t\t',randomFiveVersion(PillowTotal))

    #scikit-learn
    ScikitLearnTotal=65
    print('scikit-learn:\t',randomFiveVersion(ScikitLearnTotal))

    #matplotlib
    MatplotlibTotal=23
    print('matplotlib:\t',randomFiveVersion(MatplotlibTotal))

    #redis-py
    RedispyTotal=44
    print('redis-py:\t',randomFiveVersion(RedispyTotal))

    #tornado
    TornadoTotal=56
    print('tornado:\t',randomFiveVersion(TornadoTotal))

    #networkx
    NetworkxTotal=59
    print('networkx:\t',randomFiveVersion(NetworkxTotal))

    #rich
    RichTotal=182
    print('rich:\t\t',randomFiveVersion(RichTotal))

    #tensorflow
    TensorflowTotal=106
    print('tensorflow:\t',randomFiveVersion(TensorflowTotal))

    #fastapi
    FastapiTotal=195
    print('fastapi:\t',randomFiveVersion(FastapiTotal))

    #httpx
    HttpxTotal=74
    print('httpx:\t\t',randomFiveVersion(HttpxTotal))

    #transformer
    TransformerTotal=176
    print('transformer:\t',randomFiveVersion(TransformerTotal))

    #django
    DjangoTotal=320
    print('django:\t\t',randomFiveVersion(DjangoTotal))

    #xgboost
    XgboostTotal=51
    print('xgboost:\t',randomFiveVersion(XgboostTotal))

    #keras
    KerasTotal=54
    print('keras:\t\t',randomFiveVersion(KerasTotal))
    
    #pytorch
    PytorchTotal=57
    print('pytorch:\t',randomFiveVersion(PytorchTotal))

    #plotly.py
    PlotlypyTotal=150
    print('plotly.py:\t',randomFiveVersion(PlotlypyTotal))

    #sympy
    SympyTotal=30
    print('sympy:\t\t',randomFiveVersion(SympyTotal))

    #dask
    DaskTotal=195
    print('dask:\t\t',randomFiveVersion(DaskTotal))

    #polars
    PolarsTotal=162
    print('polars:\t\t',randomFiveVersion(PolarsTotal))

    #loguru
    LoguruTotal=22
    print('loguru:\t\t',randomFiveVersion(LoguruTotal))

    #lightGBM
    LightgbmTotal=33
    print('lightGBM:\t',randomFiveVersion(LightgbmTotal))

    #spaCy
    SpacyTotal=109
    print('spaCy:\t\t',randomFiveVersion(SpacyTotal))

    #gensim
    GensimTotal=80
    print('gensim:\t\t',randomFiveVersion(GensimTotal))

    #jax
    JaxTotal=115
    print('jax:\t\t',randomFiveVersion(JaxTotal))

    #aiohttp
    AiohttpTotal=197
    print('aiohttp:\t',randomFiveVersion(AiohttpTotal))

    #faker
    FakerTotal=432
    print('faker:\t\t',randomFiveVersion(FakerTotal))