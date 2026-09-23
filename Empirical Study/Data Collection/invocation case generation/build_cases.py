import os
from dotenv import load_dotenv, find_dotenv # 导入 find_dotenv 帮助定位
import pandas as pd
from openai import OpenAI
import httpx
import logging


def check_loading_config():
    print("--- 开始 .env 文件加载调试 ---")
    dotenv_path_found = find_dotenv(usecwd=True) # 检查当前工作目录
    if not dotenv_path_found:
        dotenv_path_found = find_dotenv() # 如果CWD没有，则按标准方式查找（从脚本目录向上）

    if dotenv_path_found:
        loaded_successfully = load_dotenv(dotenv_path=dotenv_path_found, verbose=True, override=True)
        if loaded_successfully:
            print("DEBUG: 成功从 .env 文件加载变量。")
        else:
            print("DEBUG: .env 文件已找到，但 load_dotenv() 执行完毕 (请检查 verbose 输出和后续变量值)。")
    else:
        raise RuntimeError("DEBUG: 未能找到 .env 文件。")

    # 1. 从环境变量加载 API 密钥和基础 URL
    api_key = os.getenv("OPENAI_API_KEY")
    base_url_from_env = os.getenv("OPENAI_BASE_URL")

    if not api_key:
        raise RuntimeError("错误：未能从 .env 文件或环境变量中获取 OPENAI_API_KEY。")

    return base_url_from_env, api_key

def extract_text_from_response(response):
    text = getattr(response, "output_text",None)
    if isinstance(text, str) and text:
        return text
    texts = []
    for item in getattr(response, "output", []):
        for content in getattr(item, "content", []):
            # content.type 通常是 "output_text" 或 "text"
            text_obj = getattr(content, "text", None)
            if isinstance(text_obj, str):
                texts.append(text_obj)
            elif hasattr(text_obj, "value"):
                texts.append(text_obj.value)
    return "\n".join(texts)

def askLLM(base_url, api_key, prompt,library_name,version,fully_qualified_name):

    prompt = prompt.format(
        library_name=library_name,
        version=version,
        fully_qualified_name=fully_qualified_name
    )

    client = OpenAI(
        api_key = api_key,
        base_url = base_url,
        timeout=httpx.Timeout(300.0, connect=60.0),
        max_retries=1,
    )

    messages_payload = [
        {
            "role": "system",
            "content": prompt
        }
    ]

    tool_payload = [
        {
            "type":"web_search"
        }
    ]
    try:
        response = client.responses.create(
            model = "gpt-4o-2024-08-06",
            input = messages_payload,
            tools = tool_payload,
            tool_choice = "auto",
            temperature=0.1
        )
    except Exception as e:
        logging.error(
            "%s/%s@%s: %s",
            library_name,
            fully_qualified_name,
            version,
            type(e).__name__
        )
        #return prompt   #tochange2
        return ""
    return extract_text_from_response(response)
    

def task(prompt_template,version,fully_qualified_name,url,key, output_base,library_name):

    result = askLLM(url, key, prompt_template,library_name,version,fully_qualified_name)

    output_path = output_base+'/'+library_name+'/'+ fully_qualified_name+"@"+version+"/"+fully_qualified_name+".py"
    while(os.path.exists(output_path)):
        logging.error("重复输出路径：%s", output_path)
        output_path = output_path.replace(".py","_z.py")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    lines = result.splitlines()
    if len(lines)<=2:
        logging.error("%s: 返回结果可能有误（行数过少）", output_path)
    elif lines[0].strip().startswith("```"):
        lines = lines[1:-1]
    with open(output_path, "w", encoding="utf-8") as f:
        f.write('\n'.join(lines))


def main():
    url,key = check_loading_config()
    prompt_path = "prompt.txt"
    excel_path = "build_cases_input.xlsx"
    output_base = "bench_new"
    log_path = "log.text"

    # excel_path = "test_data.xlsx"
    # output_base = "testbench"
    # log_path = "testlog.text"
    
    # ==================================

    logging.basicConfig(
        filename=log_path,
        filemode="w",
        level=logging.ERROR,
        format="%(asctime)s - %(levelname)s - %(message)s",
        encoding="utf-8"
    )

    # 读取 prompt 模板
    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt_template = f.read()

    # 读取 excel
    xls = pd.ExcelFile(excel_path)

    # 遍历每个 sheet，对应 library_name
    for sheet_name in xls.sheet_names:
        library_name = sheet_name
        df = pd.read_excel(excel_path, sheet_name=sheet_name)

        for idx, row in df.iterrows():
            version = str(row.iloc[0]).strip()
            if pd.isna(row.iloc[1]):
                continue
            else:
                fully_qualified_name = str(row.iloc[1]).strip()
            if fully_qualified_name=="":
                continue

            task(prompt_template,version,fully_qualified_name,url,key,output_base,library_name)


if __name__ == "__main__":
    main()