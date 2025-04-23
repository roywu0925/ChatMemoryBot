from chatlog import Session, ChatLog

session = Session()
logs = session.query(ChatLog).all()

for log in logs:
    print(f"👤 你說：{log.user_input}")
    print(f"🤖 AI 回答：{log.ai_response}")
    print("-" * 40)