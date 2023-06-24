import requests
import openai

import os
import openai
import warnings

warnings.filterwarnings('ignore')
os.environ["OPENAI_API_KEY"] = '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'
os.environ["SERPAPI_API_KEY"] = 'cd65b8f818b388dd50ef211bbc17d66eeed679b0ce57c0bbcad9f73b4e76237b'

serpapi_key = os.environ['SERPAPI_API_KEY']
openai.api_key = os.environ['OPENAI_API_KEY']
print(openai.api_key)


def search(query):
    # 构建 SERPAPI 请求
    params = {
        'api_key': serpapi_key,
        'q': query,
        'num': 5,  # 返回结果数量
        'engine': 'google',  # 搜索引擎（这里以 Google 为例）
    }
    response = requests.get('https://api.serpapi.com/search', params=params)

    # 解析 SERPAPI 响应
    if response.status_code == 200:
        data = response.json()
        search_results = data['organic_results']
        return search_results
    else:
        return []


def generate_text(prompt):
    # 使用 OpenAI GPT-3.5 生成文本
    response = openai.Completion.create(
        engine='text-davinci-003',  # 使用 GPT-3.5 引擎
        prompt=prompt,
        max_tokens=100,  # 生成文本的最大长度
        n=1,  # 只获取一个响应
        stop=None,  # 可以指定一个停止词，用于结束生成
    )

    if response and response.choices:
        return response.choices[0].text.strip()
    else:
        return ''


# 搜索并获取结果
query = 'Python programming'
results = search(query)

# 打印搜索结果
for result in results:
    print(result['title'])
    print(result['link'])
    print(result['snippet'])
    print('---')

# 使用生成文本功能
prompt = 'Translate the following English text to French: "Hello, how are you?"'
generated_text = generate_text(prompt)

# 打印生成的文本
print(generated_text)
