#Exercise 2 Sales
# Read sales.csv in dataframe.
# Calculate, for each row  amount of the sale by multiplying the quantity and the price
# Sort the dataframe by the amount of the sale in descending order
# Export the sorted dataframe to a json file
# Create a plot containing with amount of sales for each item



import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# Read sales.csv in dataframe.
sales = pd.read_csv("Dataset/sales.csv")
print(sales.head())

# Calculate, for each row  amount of the sale by multiplying the quantity and the price
sales["total price"] = sales["quantity"] * sales["price"]
print(sales.head())

# Sort the dataframe by the amount of the sale in descending order
sales_sorted = sales.sort_values(by="quantity", ascending=False)
print(sales_sorted.head())

# Export the sorted dataframe to a json file
with open('Dataset/sales.json', 'w') as json_file:
    json_file.write(sales_sorted.to_json(orient='records', lines=True))

# Create a plot containing with amount of sales for each item
grouped_sales = sales.groupby('product_id')['quantity'].sum().reset_index()
# print(grouped_sales.head())
# x = grouped_sales["product_id"]
# y = grouped_sales["quantity"]
# plt.bar(x,y)
# plt.xlabel("Product ID")
# plt.ylabel("Total Quantity Sold")
# plt.title("Total Sales by Product ID")
#
# # Mostra il grafico
# plt.show()

sns.barplot(x='product_id', y='quantity', data=grouped_sales)

# Aggiungi etichette e titolo
plt.xlabel("Product ID")
plt.ylabel("Total Quantity Sold")
plt.title("Total Sales by Product ID")

# Mostra il grafico
plt.show()