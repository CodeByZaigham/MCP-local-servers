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
def create_expense():
     pass