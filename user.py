import os
import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
engine=create_engine('postgresql://postgres:pyj@ma334@localhost:5432/user')

db=scoped_session(sessionmaker(bind=engine))

f=open('usersData.csv')
reader=csv.reader(f)
for name,email,current_credit in reader:
	db.execute("INSERT INTO users ( name,email,current_credit ) VALUES(:name,:email,:current_credit )",
		{"name" :name,"email":email,"current_credit" :current_credit})
db.commit()
