import qrcode
import sqlite3
import itertools

def show_menu():
    print("1- Show List ")
    print("2- Add New Product")
    print("3- Edit a product")
    print("4- Remove a product")
    print("5- Search a product")
    print("6- buy product")
    print("7- QRcode")
    print("8- exit")

def load_database():
    global connection
    global my_cursor
    connection=sqlite3.connect("store.db")
    my_cursor=connection.cursor()

def show_list():
    for data in my_cursor.execute("SELECT * FROM products"):
        print(data)

def add_new_product():
    global new_product_name
    global product_price
    global product_count
    new_product_name=input("Enter a new name product:")
    product_price=float(input("Enter price of new product:"))
    product_count=input("Enter count of new product")
    my_cursor.execute(f"INSERT INTO products(name,price,count) VALUES('{new_product_name}','{product_price}','{product_count}')")
    connection.commit()

def edit_product():
    
    choose=0
    id=input("enter the id product: ")
    print("1- name")
    print("2- price")
    print("3- count")
    choose=int(input("which one do you wanna edit? "))
    if choose==1:
        global new_name
        new_name=input("Enter new name of this product: ")
        my_cursor.execute(f"UPDATE products SET name='{new_name}' WHERE id='{id}'")
        connection.commit()
        print("update succesfully")
        
    elif choose==2:
        global new_price
        new_price=input("Enter new price of this product: ")
        my_cursor.execute(f"UPDATE products SET price='{new_price}' WHERE id='{id}'")
        connection.commit() 
        print("update succesfully")  
    
    elif choose==3:
        global new_count
        new_count=input("Enter new count of this product: ")
        my_cursor.execute(f"UPDATE products SET count='{new_count}' WHERE id='{id}'")
        connection.commit() 
        print("update succesfully")
        
    else:
          print("the code not found")

def remove_product():
    global id_product
    id_product=int(input("Enter id of product that you wanna delete it: "))
    my_cursor.execute(f"DELETE FROM products WHERE id='{id_product}'")
    connection.commit()
    print("the product deleted")

def search_product():
    global result
    user_name=input("enter the name of the product that you wanna to search: ")
    result=my_cursor.execute(f"SELECT * FROM products WHERE name='{user_name}'")
    product=result.fetchone()
    print(product)


def buy_product():
    global exist_product
    cart=0
    i=1
    factor_price=0
    exist_product=my_cursor.execute(f"SELECT name FROM products")
    list_exist_product=exist_product.fetchall()
    out = list(itertools.chain(*list_exist_product))
    print(out)
    while i==1:
        user_name=input("enter the name of the product that you wanna to buy: ")
        for product in out:
            if user_name==product:
                result=my_cursor.execute(f"SELECT price FROM products WHERE name='{user_name}'")
                product=result.fetchone()
                print(f"the price of {user_name} is {product}" )

                result_count=my_cursor.execute(f"SELECT count FROM products WHERE name='{user_name}'")
                product_count=result_count.fetchone()
                print(f"{product_count}pieces of {user_name} are available in the store")
                    

                number=int(input("how many will you wanna to buy? "))

                if number > int(product_count[0]):
                                print("Sorry,there are not enouph of this product")
                                break

                elif number <=int(product_count[0]):
                                factor_price = factor_price + number*int(product[0])
                                product_count=int(product_count[0]) - number
                                my_cursor.execute(f"UPDATE products SET count='{product_count}' WHERE name='{user_name}'")
                                connection.commit()
                                cart=cart+number
                                break
                                # print("price that you should pay: " , factor_price)
                                # print("sum of the products that buy them: " , cart) 

                                # i=int(input("if you wanna buy another product enter 1 else enter 0: "))

        else:
                print("sorry this prouduct not exist")
        i=int(input("if you wanna buy another product enter 1 else enter 0: "))

    print("price that you should pay: " , factor_price)
    print("sum of the products that buy them: " , cart)

def QR_code():
    global user_name
    user_name=input("enter the name of the product that you wanna to creat QRcode: ")  
    result=my_cursor.execute(f"SELECT * FROM products WHERE name='{user_name}'")
    product=result.fetchall()
    img=qrcode.make(product)
    img.save("QRcode.png")
    
load_database()
while 1==1:

    show_menu()
    user_choice=int(input("Enter your choice: "))
    if user_choice==1:
        show_list()
        
    elif user_choice==2:
        add_new_product()
        
    elif user_choice==3:
        edit_product()
        
    elif user_choice==4:
        remove_product()

    elif user_choice==5:
        search_product()

    elif user_choice==6:
        buy_product()

    elif user_choice==7:
        QR_code()

    elif user_choice==8:
        exit(0)
