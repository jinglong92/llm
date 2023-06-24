from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI

import os
import openai
import warnings

warnings.filterwarnings('ignore')
os.environ["OPENAI_API_KEY"] = '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'
os.environ["SERPAPI_API_KEY"] = 'cd65b8f818b388dd50ef211bbc17d66eeed679b0ce57c0bbcad9f73b4e76237b'

openai.api_key = os.environ['OPENAI_API_KEY']
print(openai.api_key)

llm = OpenAI(model_name="text-davinci-003")

# 告诉他我们生成的内容需要哪些字段，每个字段类型式啥
response_schemas = [
    ResponseSchema(name="bad_string", description="This a poorly formatted user input string"),
    ResponseSchema(name="good_string", description="This is your response, a reformatted response")
]

# 初始化解析器
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

# 生成的格式提示符
# {
#	"bad_string": string  // This a poorly formatted user input string
#	"good_string": string  // This is your response, a reformatted response
# }
format_instructions = output_parser.get_format_instructions()

template = """
You will be given a poorly formatted string from a user.
Reformat it and make sure all the words are spelled correctly

{format_instructions}

% USER INPUT:
{user_input}

YOUR RESPONSE:
"""

# 将我们的格式描述嵌入到 prompt 中去，告诉 llm 我们需要他输出什么样格式的内容
prompt = PromptTemplate(
    input_variables=["user_input"],
    partial_variables={"format_instructions": format_instructions},
    template=template
)

promptValue = prompt.format(user_input="welcom to califonya!")
llm_output = llm(promptValue)

# 使用解析器进行解析生成的内容
print(output_parser.parse(llm_output))
