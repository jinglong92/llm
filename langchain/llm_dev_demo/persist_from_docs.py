from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import DirectoryLoader
from langchain.vectorstores import Chroma, Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain

# pip3 install pinecone-client
import pinecone

import os
import openai
import warnings

warnings.filterwarnings('ignore')
os.environ["OPENAI_API_KEY"] = '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'
os.environ["SERPAPI_API_KEY"] = 'cd65b8f818b388dd50ef211bbc17d66eeed679b0ce57c0bbcad9f73b4e76237b'

openai.api_key = os.environ['OPENAI_API_KEY']
print(openai.api_key)

# 初始化 pinecone
# Pinecone 是一个在线的向量数据库。https://app.pinecone.io/
pinecone.init(
    api_key="d07c1020-f934-44c9-94f6-52f5d80bfcb6",
    environment="us-west1-gcp-free"
)

loader = DirectoryLoader('/langchain/data', glob='**/*.txt')
# 将数据转成 document 对象，每个文件会作为一个 document
documents = loader.load()

# 初始化加载器
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0)
# 切割加载的 document
split_docs = text_splitter.split_documents(documents)

index_name = "liaokong-test"

# 初始化 openai 的 embeddings 对象
embeddings = OpenAIEmbeddings()

# 方式 1：Pinecone 是一个在线的向量数据库。所以，我可以第一步依旧是注册，然后拿到对应的 api key。https://app.pinecone.io/
# 持久化数据
# docsearch = Pinecone.from_texts([t.page_content for t in split_docs], embeddings, index_name=index_name)

# 加载数据
# docsearch = Pinecone.from_existing_index(index_name, embeddings)

# 方式 2：chroma 是个本地的向量数据库，他提供的一个 persist_directory 来设置持久化目录进行持久化。读取时，只需要调取 from_document 方法加载即可。
# 持久化数据
docsearch = Chroma.from_documents(documents, embeddings,
                                  persist_directory="/Users/xuduobao/meituan/llm/langchain/data/vector_store")
docsearch.persist()

# 加载数据
docsearch = Chroma(persist_directory="/Users/xuduobao/meituan/llm/langchain/data/vector_store",
                   embedding_function=embeddings)

# query = "科大讯飞今年第一季度收入是多少？"
query = "AIGB是什么？"

docs = docsearch.similarity_search(query)

llm = OpenAI(temperature=0)
chain = load_qa_chain(llm, chain_type="stuff", verbose=True)
results = chain.run(input_documents=docs, question=query)
print(results)
