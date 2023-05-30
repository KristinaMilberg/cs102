# создание шаблона базы данных
from scraputils import get_news
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()  # type: ignore
engine = create_engine("sqlite:///news.db")  # type: ignore
session = sessionmaker(bind=engine)

# создаем таблицу на локальном хосте
class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    url = Column(String)
    comments = Column(Integer)
    points = Column(Integer)
    label = Column(String)


Base.metadata.create_all(bind=engine)

if __name__ == "__main__":  # создаем сессию, подключаем новости, классификатор их нумерует и заполняет таблицу, такая же схема коммита как в гите
    a = session()
    news_list = get_news("https://news.ycombinator.com/newest", n_pages=35)
    for k in range(len(news_list)):
        news = News(
            title=news_list[k]["title"],
            author=news_list[k]["author"],
            url=news_list[k]["url"],
            comments=news_list[k]["comments"],
            points=news_list[k]["points"],
        )
        a.add(news)
        a.commit()