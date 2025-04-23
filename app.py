from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import ConversationChain
from langchain_community.chat_models import ChatOpenAI as CommunityChatOpenAI
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain.memory import ConversationBufferMemory
from dotenv import dotenv_values
from chatlog import Session, ChatLog

config = dotenv_values(".env")
llm = ChatOpenAI(api_key=config.get("OPENAI_API_KEY"), model="gpt-4o")

message_history = RedisChatMessageHistory(
    session_id="my-session",
    url="redis://localhost:6379"
)
memory = ConversationBufferMemory(memory_key="history", chat_memory=message_history, return_messages=True)
conversation = ConversationChain(llm=llm, memory=memory)

print("你想問 AI 什麼？（輸入 'bye' 結束）：")
while True:
    user_input = input("\n你：")
    if user_input.lower() == "bye":
        break
    if user_input == "/紀錄":
        # 顯示所有對話紀錄（這段邏輯會阻擋傳入 AI）
        session = Session()
        logs = session.query(ChatLog).all()
        for log in logs:
            print(f"👤 你說：{log.user_input}")
            print(f"🤖 AI 回答：{log.ai_response}")
            print("-" * 40)
        continue

    answer = conversation.predict(input=user_input)
    print("\n🤖 AI：", answer)

    # 儲存對話進資料庫
    session = Session()
    chat = ChatLog(user_input=user_input, ai_response=answer)
    session.add(chat)
    session.commit()