import os
import warnings

import openai
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain

warnings.filterwarnings('ignore')
os.environ["OPENAI_API_KEY"] = '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'

openai.api_key = os.environ['OPENAI_API_KEY']
print(openai.api_key)

from langchain.document_loaders import TextLoader

loader = TextLoader("/langchain/data/vec.txt")
documents = loader.load()

# 将文档拆分、创建嵌入并将它们放入向量存储中
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
documents = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(documents, embeddings)

from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)


def get_chat_history(inputs) -> str:
    res = []
    for human, ai in inputs:
        res.append(f"Human:{human}\nAI:{ai}")
    return "\n".join(res)


qa = ConversationalRetrievalChain.from_llm(OpenAI(temperature=0), vectorstore.as_retriever(),
                                           get_chat_history=get_chat_history)

chat_history = []
while True:
    query = input('问题：')
    # query = "AIGB是什么？"
    result = qa({"question": query, "chat_history": chat_history})
    chat_history.append((query, result["answer"]))

    # 根据特定的prompt生成格式化输出
    prompt = "Code Formatting Template:\n{}\n\n"
    promptValue = prompt.format(chat_history[-1])
    print(promptValue)
