
import os
import openai
import warnings

warnings.filterwarnings('ignore')
os.environ["OPENAI_API_KEY"] = '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'
os.environ["SERPAPI_API_KEY"] = 'cd65b8f818b388dd50ef211bbc17d66eeed679b0ce57c0bbcad9f73b4e76237b'

openai.api_key = os.environ['OPENAI_API_KEY']
print(openai.api_key)

import os

os.environ["ZAPIER_NLA_API_KEY"] = 'sk-ak-H0vg9trXpkEDHRXCnk9a8aYyfq'

from langchain.llms import OpenAI
from langchain.agents import initialize_agent
from langchain.agents.agent_toolkits import ZapierToolkit
from langchain.utilities.zapier import ZapierNLAWrapper

llm = OpenAI(temperature=.3)

# 我们主要是结合使用 zapier 来实现将万种工具连接起来。https://zapier.com/l/natural-language-actions
zapier = ZapierNLAWrapper()
toolkit = ZapierToolkit.from_zapier_nla_wrapper(zapier)
agent = initialize_agent(toolkit.get_tools(), llm, agent="zero-shot-react-description", verbose=True)

# 我们可以通过打印的方式看到我们都在 Zapier 里面配置了哪些可以用的工具
for tool in toolkit.get_tools():
    print(tool.name)
    print(tool.description)
    print("\n\n")

agent.run('请用中文总结最后一封"jinglong92@163.com"发给我的邮件。并将总结发送给"jinglong92@163.com"')
