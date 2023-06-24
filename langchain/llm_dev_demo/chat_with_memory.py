import os
import warnings

import openai
from langchain import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.memory import ChatMessageHistory

warnings.filterwarnings('ignore')
os.environ["OPENAI_API_KEY"] = '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'
os.environ["SERPAPI_API_KEY"] = 'cd65b8f818b388dd50ef211bbc17d66eeed679b0ce57c0bbcad9f73b4e76237b'

openai.api_key = os.environ['OPENAI_API_KEY']
print(openai.api_key)
chat = ChatOpenAI(temperature=0)

prompt_template = """
Use the following context to answer the user's question.
If you don't know the answer, say you don't, don't try to make it up. And answer in Chinese.

I want you to act as an IT Expert. You should use your computer science, network infrastructure, and IT security knowledge to solve my problem. 
Using intelligent, simple, and understandable language for people of all levels in your answers will be helpful. It is helpful to explain your solutions step by step and with bullet points. Try to avoid too many technical details, but use them when necessary. I want you to reply with the solution, not write any explanations. 

-----------
{context}
-----------
{chat_history}
"""

# 初始化 MessageHistory 对象
chat_history = ChatMessageHistory()

# 给 MessageHistory 对象添加对话内容
chat_history.add_ai_message("Hi！")
# history.add_user_message("中国的首都是哪里？")
# history.add_ai_message("中国的首都是北京。")
chat_history.add_user_message(
    "I have a class.mthod :public static BiddingResponse dualBidding(@NonNull BiddingRequest biddingRequest), which will be called by a few applications, How should i design my program to make it better")
chat_history.add_ai_message("""To design your program and improve the dualBidding method, you can consider the following recommendations:
Encapsulation: Encapsulate the functionality of the dualBidding method within a class dedicated to handling bidding operations. This promotes modularity and separation of concerns.
Input Validation: Validate the biddingRequest parameter to ensure it meets the required criteria before processing it. Check for null values, required fields, and appropriate data types.
Error Handling: Implement robust error handling to handle exceptions and unexpected scenarios gracefully. Provide informative error messages or error codes to aid in troubleshooting.
Logging: Implement logging within the method to track and monitor the execution flow, important events, and potential issues. This can help with debugging and performance analysis.
Performance Optimization: Consider potential optimizations to improve the performance of the method, such as reducing unnecessary computations, optimizing data structures, or caching frequently accessed data.
Security Considerations: If the BiddingRequest or any associated data involves sensitive information, ensure proper security measures are in place, such as data encryption, access controls, and input sanitization to prevent security vulnerabilities.
Code Documentation: Document the purpose, inputs, outputs, and any assumptions made by the dualBidding method. Use clear and meaningful method and parameter names to enhance code readability.
Unit Testing: Create unit tests to verify the correctness of the dualBidding method under different scenarios and edge cases. This ensures reliability and helps catch any regressions during future development.
By following these guidelines, you can enhance the design and functionality of your program while considering important aspects such as encapsulation, validation, error handling, performance, security, documentation, and testing.""")
chat_history.add_user_message("uh, actually i want you to help me design it using some tricks like abstract method")


# 执行对话
ai_response = chat(chat_history.messages)

# 根据特定的prompt生成格式化输出
prompt = "Code Formatting Template:\n\n{}\n\nAI Response:\n\n{}"
promptValue = prompt.format(chat_history.messages, ai_response.content)
print(promptValue)
