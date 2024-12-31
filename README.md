***WELCOME TO THE ECOMMERCE MINI PROJECT***

-OVERVIEW-

This project has been designed to utilize Postman to create a database to hold information about Customers including (name, email, date of birth, and addresses), 
User Accounts including (username and passwords), Orders including (order dates, status of order, date order is closed, and the total of the order), and Products
including (name/description, the par inventory to be kept on hand, the current inventory, and the product price.)

--Utilizing User Routes--

In Postman enter http://127.0.0.1:5000/customers into the URL bar.

-Get all customer information
-GET Customers-
    -Select the GET method from the drop down menu and click "Send"
    -All customers held in the database will be shown in the body.

-Add a new customer
-POST Customer-
    -Select the POST method from the drop down menu and click "Send"
-This will allow you to add a new customer to the database.
    -Enter the customer information in the following format.
    {
        "address": "Input Customer Address",
        "date_of_birth": "Input Customer's Date of Birth",
        "email": "Input Customer's Email",
        "name": "Input Customer's Name"
    }
    -After click Send to add the information to the database.

In Postman enter http://127.0.0.1:5000/customers/id# into the URL bar.
-Update a customer's information
-PUT Customer-
    -Select the PUT method from the drop down menu and click "Send"
-This route allows you to update customer information.
-The URL is the same but after "/customers" you will need to enter "/customer's id#". 

    Enter the customer information in the following format with any information you would like changed
    {
        "address": "Input Customer Address",
        "date_of_birth": "Input Customer's Date of Birth",
        "email": "Input Customer's Email",
        "name": "Input Customer's Name"
    }

-Delete a customer's information
-DELETE Customer-
    -Select the DELETE method from the drop down menu and click "Send"
-This route allows you to DELETE a customer from the database.
    -Again you will need the ID# of the customer for deletion
    -The URL is the same but after "/customers" you will need to enter "/customer's id#".


--Utilizing Customer Account Routes--

In Postman enter http://127.0.0.1:5000/customer_accounts into the URL bar.


-Get all customer account information
-GET Customer Accounts-
    -Select the GET method from the drop down menu and click "Send"
    -All customer accounts held in the database will be shown in the body.

-Add a customer account
-POST Customer Account
    -This will allow you to add a customer.
    -The format for this is below.
    {
        "customer_id": # of the user this account is tied to,
        "password": "UsersPassword",
        "username": "Unique Username"
    }
    -Select the POST method from the drop down menu and click "Send"

-Update a customer account
-In Postman enter http://127.0.0.1:5000/customer_accounts/id into the URL bar.
-PUT Customer account
    -This will allow you to update a customer's account information
    -Again you will need to know the customer account id# (not to be confused with the customer_id it is tied to.)
    -The URL is the same but after "/customer_accounts" you will need to enter "/customer_accounts id#". 
    -Enter the same format as if you were going to make a new customer under this URL
        {
            "customer_id": # of the user this account is tied to,
            "password": "UsersPassword",
            "username": "Unique Username"
        }
    -Select the PUT method from the drop down menu and click "Send"


-Delete a customer account from the database
-DELETE Customer Account-
    -Select the DELETE method from the drop down menu and click "Send"
-This route allows you to DELETE a customer from the database.
    -Again you will need the ID# of the customer for deletion
    -The URL is the same but after "/customer_accounts" you will need to enter "/customer_accounts id#".


--Utilizing Orders Routes--

-In Postman enter http://127.0.0.1:5000/orders into the URL bar.
-Get all orders information
-GET Orders-
    -Select the GET method from the drop down menu and click "Send"
    -All orders held in the database will be shown in the body.

-Add orders to the database.
-POST Orders-

-This is the format to enter a new order.
{
    "order_date": "Date Order is created",
    "status": "Enter current status of the order",
    "close_date": "Date order was completed", (This can be omitted)
    "product_ids": [Product ID #'s separated by commas (ex. [1,2,3])],
    "account_id": ID# of the customer account
}

-Select the POST method from the drop down menu and click "Send"

-Update Orders-
-In Postman enter http://127.0.0.1:5000/orders/id# into the URL bar.
-Here you can update an order with any and all new information.
-The format for submission is the same as 'POST' orders and you will need
the order id# to enter into the URL bar the same as for 'customers' and customer accounts'
-Select the PUT method from the drop down menu and click "Send"

=Delete Orders-
-This format will follow the DELETE Customers and Customer Accounts.
-You will need the order_id that you wish to delete and add that to the end of the orders URL again.
-In Postman enter http://127.0.0.1:5000/orders/id# into the URL bar.
-Select the DELETE method from the drop down menu and click "Send"


--Utilizing Products Routes--
This will follow the same formating for the Routes to Get all products, Add a new product, Update a product, Delete a product
as the previous routes.

The URL for this is as follows for the GET and POST methods
-In Postman enter http://127.0.0.1:5000/products into the URL bar.
-The format to enter a new product is as follows.

{
    "name": "Name of product/description",
    "par_inventory": # of products to be kept on hand at all times,
    "current_inventory": Current number of products held,
    "price": Price of product to be charged to the customer
}

The following is the URL for the PUT (to update a product) method and the DELETE a product method.
-In Postman enter http://127.0.0.1:5000/products/id# into the URL bar.