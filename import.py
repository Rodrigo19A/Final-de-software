import csv
from run import Products
from run import db

def main():
    with open("products.csv", "r") as f:
        reader = csv.reader(f)
        for name, price, description in reader:
            product = Products(name=name, price=price, description=description)
            db.session.add(product)
            print(f"Added product {name}, {price}, {description}")
        db.session.commit()

if __name__ == "__main__":
    main()
