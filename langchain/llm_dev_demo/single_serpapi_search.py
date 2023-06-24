import os
import warnings

import openai

warnings.filterwarnings('ignore')

os.environ["OPENAI_API_KEY"] = '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'
os.environ["SERPAPI_API_KEY"] = 'cd65b8f818b388dd50ef211bbc17d66eeed679b0ce57c0bbcad9f73b4e76237b'

openai.api_key = os.environ['OPENAI_API_KEY']
print(openai.api_key)

from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI
from langchain.agents import AgentType
from langchain import LLMMathChain, SerpAPIWrapper

# 加载 OpenAI 模型
llm = OpenAI(temperature=0, max_tokens=1024)

# 加载 serpapi 工具
# tools = load_tools(["serpapi"])

# 方法 1：如果搜索完想再计算一下可以这么写
# tools = load_tools(['serpapi', 'llm-math'], llm=llm)

# 方法 2：也可以自定义agent中所使用的工具
search = SerpAPIWrapper()
llm_math_chain = LLMMathChain(llm=llm, verbose=True)

# 创建一个功能列表，指明这个 agent 里面都有哪些可用工具，agent 执行过程可以看必知概念里的 Agent 那张图
tools = [
    Tool(
        name="Search",
        func=search.run,
        description="useful for when you need to answer questions about current events"
    ),
    # 自定义工具里面有个比较有意思的地方，使用哪个工具的权重是靠工具中描述内容来实现的，和我们之前编程靠数值来控制权重完全不同。
    Tool(
        name="Calculator",
        func=llm_math_chain.run,
        description="useful for when you need to answer questions about math"
    )
]

# 如果搜索完想再让他再用python的print做点简单的计算，可以这样写
# tools=load_tools(["serpapi","python_repl"])

# 工具加载后都需要初始化，verbose 参数为 True，会打印全部的执行详情
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

# 运行 agent
# results = agent.run("What's the date today? What great events have taken place today in history?")
# results = agent.run("哪里妖气最重?")
results = agent.run("Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?")

print(results)
