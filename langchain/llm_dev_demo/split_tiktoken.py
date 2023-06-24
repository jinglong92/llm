import os
import openai
import warnings

warnings.filterwarnings('ignore')
os.environ["OPENAI_API_KEY"] = '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'
os.environ["SERPAPI_API_KEY"] = 'cd65b8f818b388dd50ef211bbc17d66eeed679b0ce57c0bbcad9f73b4e76237b'

openai.api_key = os.environ['OPENAI_API_KEY']
print(openai.api_key)

from langchain.document_loaders import UnstructuredFileLoader
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain import OpenAI

# 导入文本
loader = UnstructuredFileLoader("/langchain/data/lg_test.txt")
# 将文本转成 Document 对象
document = loader.load()
print(f'original documents:{len(document)}')

# 初始化文本分割器
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=0
)

# 切分文本
split_documents = text_splitter.split_documents(document)
print(f'splitted documents:{len(split_documents)}')

# 加载 llm 模型
llm = OpenAI(model_name="text-davinci-003", max_tokens=1500)

# 创建总结链
# chain_type 这个参数主要控制了将 document 传递给 llm 模型的方式，一共有 4 种方式
chain = load_summarize_chain(llm, chain_type="map_reduce", verbose=True)   # chain_type="refine" 序列化

# 执行总结链，（为了快速演示，只总结前5段）
results = chain.run(split_documents[:5])
print(results)
