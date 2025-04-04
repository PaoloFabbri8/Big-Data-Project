import duckdb
con = duckdb.connect()

sales = con.execute("SELECT * FROM 'Dataset/sales.csv'").df()
print(sales)
#read json products
products = con.execute("SELECT * FROM 'Dataset/products.json'").df()
print(products)

#Find all the sales entry for the product with id ‘21’. Export them to a new csv file sales21.csv
Prod21 = con.execute("SELECT * FROM sales WHERE product_id = 21").df()
print(Prod21)
Prod21.to_csv('Dataset/sales21.csv', index=False)

#Find the 10 most recent sales. Export them to the file top10.json
recent_sales = con.execute("SELECT * FROM sales ORDER BY dt Desc LIMIT 10").df()
print(recent_sales)

recent_sales.to_json('Dataset/top10.json', orient='records', lines=True)

#For each product, calculates how many units were sold in total. Export the to product_unit.csv
total_prod = con.execute("SELECT product_id, sum(quantity) as total_unit FROM sales GROUP BY product_id").df()
print(total_prod)

total_prod.to_csv('Dataset/product_unit.csv', index=False)

#For each category find how many units where sold in total. Export the to category_unit.csv
con.execute("CREATE TABLE sales_prod AS SELECT * FROM sales INNER JOIN products ON sales.product_id = products.product_id")
category_unit = con.execute("SELECT category, SUM(quantity) AS total_unit FROM sales_prod GROUP BY category").df()
print(category_unit)

#category_unit.to_csv("category_unit.csv", index=False)
category_unit.to_csv('Dataset/category_unit.csv', index=False)

#Update the category of the item “Desk” to “Office”
con.execute("CREATE TABLE products AS SELECT * FROM read_json('Dataset/products.json')")
con.execute("UPDATE products SET category = 'Office' WHERE name = 'Desk'")
print(products)

#Delete all sales for category “Sneakers”
con.execute("DELETE FROM sales_prod WHERE name = 'Sneakers'")
print(con.execute("SELECT * FROM sales_prod").df())