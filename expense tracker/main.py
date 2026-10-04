from fastmcp import FastMCP
import os
import sqlite3

mcp=FastMCP(name="expense tracking server")

database=os.path.join(os.path.dirname(__file__),"expenses.db")
CATEGORIES=os.path.join(os.path.dirname(__file__),"categories.json")

with sqlite3.connect(database) as d:
     d.execute("""
          CREATE TABLE IF NOT EXISTS expenses(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          date TEXT NOT NULL,
          amount REAL NOT NULL,
          category TEXT NOT NULL,
          subcategory TEXT DEFAULT '',
          note TEXT DEFAULT ''
          )
     """)

@mcp.tool
def create_expense(date,amount,category,subcategory,note):
     "add a new expense to the database"
     with sqlite3.connect(database) as d:
          result=d.execute(
               "INSERT INTO expenses(date, amount, category, subcategory, note) VALUES (?,?,?,?,?)",
               (date, amount, category, subcategory, note)
          )
     return {"status":"ok" , "id":result.lastrowid}

@mcp.tool
def list_expenses(start_date, end_date):
     "list all expenses for the given time period"
     with sqlite3.connect(database) as d:
          result=d.execute("""
               select date, amount, category, subcategory, note from expenses 
               where date between ? and ? 
               orderby id asc
          """,(start_date, end_date))
     cols = [d[0] for d in result.description]
     return [dict(zip(cols, r)) for r in result.fetchall()]

@mcp.tool
def summarize(start_date, end_date,category=None):
     "summarize all expenses done in a given time period"
     query="select category , sum(amount) from expenses where date between ? and ? orderby category asc"
     params=[start_date, end_date]
     if category:
          query+=" and category=?"
          params.append(category)
     query+="group by category order by category asc"
     with sqlite3.connect(database) as d:
          result=d.execute(query,params)
     cols = [d[0] for d in result.description]
     return [dict(zip(cols, r)) for r in result.fetchall()]

@mcp.resource("expense://categories",mime_type="application/json")
def categories():
     "read categories and sub categories of expenses"
     with open(CATEGORIES,"r") as f:
          return f.read()

if __name__ == "__main__":
     mcp.run()

