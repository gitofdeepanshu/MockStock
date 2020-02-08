from app import create_app, db
from app.models import Stock

import csv
import sys

if len(sys.argv) > 1:
    CSV_FILE = sys.argv[1]
else:
    CSV_FILE = "/home/oreki/Downloads/stocks.csv"

print("Loading data from - " + CSV_FILE)

app = create_app()
app_context = app.app_context()
app_context.push()

with open(CSV_FILE, newline='') as f:
    print("Rows Deleted from Stocks - " + str(Stock.query.delete()))
    reader = csv.reader(f)
    for i,row in enumerate(list(reader)[2:]):
        if i % 2 ==0:
            stk = Stock(name=row[0], price=row[3], region=row[1], type=row[2])
            db.session.add(stk)
            print("Added - " + str(row))
    db.session.commit()
