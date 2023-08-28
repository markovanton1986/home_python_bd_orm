import sqlalchemy
from sqlalchemy.orm import sessionmaker
import json

from models import create_tables, Publisher, Sale, Book, Stock, Shop

SQLsystem = 'postgresql'
login = ''
password = ''
host = 'localhost'
port = 5432
db_name = "2"
DSN = f'{SQLsystem}://{login}:{password}@{host}:{port}/{db_name}'
engine = sqlalchemy.create_engine(DSN)

Session = sessionmaker(bind=engine)
session = Session()

create_tables(engine)

with open('tests_data.json', 'r') as db:
    data = json.load(db)

for line in data:
    method = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[line['model']]
    session.add(method(id=line['pk'], **line.get('fields')))

session.commit()

writer = input('Введите имя писателя или id: ')
query = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).join(Publisher).join(Stock).join(Shop).join(Sale)
if writer.isdigit():
    query = query.filter(Publisher.id == writer).all()
else:
    query = query.filter(Publisher.name == writer).all()

for title, name, price, date_sale in query:
    print(f"{title:<40} | {name:<10} | {price:<8} | {date_sale}")

session.close()