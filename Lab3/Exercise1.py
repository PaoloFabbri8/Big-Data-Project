#Exercise 1 Books
# Using the books.json file:
# load the file in a pandas dataframe
# how many rows and columns do you get?
# export the book from Gabriel Garcia Marquez in a dedicate csv file
# remove all the book from George Orwell
# which is the author that has more publications?
import pandas as pd

# Load JSON file
df = pd.read_json("Dataset/books.json")

# Display number of rows and columns
print(df.head())
rows, cols = df.shape
print(f"Rows: {rows}, Columns: {cols}")

# Filter books by Gabriel Garcia Marquez
marquez_books = df[df['author'] == "Gabriel Garcia Marquez"]

# Export to CSV
marquez_books.to_csv("gabriel_garcia_marquez_books.csv", index=False)

print("CSV file for Gabriel Garcia Marquez's books saved.")

# Remove all the book from George Orwell
df = df[df['author'] != "George Orwell"]

#Which is the author that has more publications?
author = df['author'].value_counts().idxmax()
print(f"Author with most publications: {author}")