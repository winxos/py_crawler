from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()


class Items(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(30))
    author = Column(String(30))
    title = Column(String(100))
    url = Column(String(100))


def init_db():
    engine = create_engine('sqlite:///test.db')
    engine.echo = False  # Try changing this to True and see what happens
    DBSession = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    Session = DBSession()
    n = Items(title="adsf", url="ooo")
    Session.add(n)
    Session.commit()
    Session.close()


if __name__ == '__main__':
    init_db()
