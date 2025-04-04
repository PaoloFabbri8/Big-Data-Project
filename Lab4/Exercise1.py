import duckdb

con = duckdb.connect()
con.execute("CREATE TABLE users (id INTEGER, name TEXT, age INTEGER)")
con.execute("INSERT INTO users VALUES (1, 'Alice', 25), (2, 'Bob', 30)")

result = con.execute("SELECT * FROM users").fetchall()
print(result)

#As Pandas dataframe
resultdata = con.execute("SELECT * FROM 'sales.csv' LIMIT 10").fetchall()
print(resultdata)

df = con.execute("SELECT * FROM 'sales.csv' LIMIT 10").df()
df

