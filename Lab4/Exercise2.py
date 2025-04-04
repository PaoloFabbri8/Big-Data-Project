import duckdb
con = duckdb.connect()

sales = con.execute("SELECT * FROM 'sales.csv' LIMIT 10").df()
print(sales)


con.execute("SELECT * FROM sales").df().info()

con.execute("CREATE TABLE sales_users AS SELECT * FROM 'sales.csv' INNER JOIN users ON sales.user_id = users.id").df().info()
print(con.execute("SELECT * FROM sales_users LIMIT 10").df())