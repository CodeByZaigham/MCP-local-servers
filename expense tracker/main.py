from fastmcp import FastMCP
import os
import sqlite3

mcp=FastMCP(name="expense tracking server")

database=os.path.join(os.path.dirname(__file__),"expenses.db")

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
          result=d.execute("""
               "INSERT INTO expenses(date, amount, category, subcategory, note) VALUES (?,?,?,?,?)",
               (date, amount, category, subcategory, note)
          """)
     return {"status":"ok" , "id":result.lastrowid}

