from sqlalchemy import Column, Integer, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class ChatLog(Base):
    __tablename__ = "chatlogs"
    id = Column(Integer, primary_key=True)
    user_input = Column(Text)
    ai_response = Column(Text)

engine = create_engine("sqlite:///chatlogs.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)