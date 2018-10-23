# Store Manager


## Introduction

Store Manager is a web application that helps store owners manage sales and product inventory records. This application is meant for use in a single store.

### Features

1. Admin can add a product.
2. Admin/store attendant can get all products
3. Admin/store attendant can get a specific product
4. Store attendant can add a sale order
5. Admin can get all sale records

### Installing

*Step 1*

Create directory
```$ mkdir store_manager_api```

```$ cd store_manager_api```

create a .env file

``` touch .env```
``` using the .env_example as an example, add details to the .env file```

Create and activate virtual environment

```$ virtualenv env -p python3```


```$ source env/bin/activate ```

Clone the repository [```here```](https://github.com/waracci/store-manager-v2) or 

``` git clone https://github.com/waracci/store-manager-v2 ```

Install project dependencies 


```$ pip install -r requirements.txt```


*Step 2* 

#### Set up database and virtual environment & Database 

``` Using the command on the terminal```
> Create two databases: store and test_store

*Step 3*

#### Storing environment variables 

```
environment variables are stored in .env file
```

*Step 4*

#### Running the application

```$ flask run``` 

*Step 5*

#### Testing

```$ python manage.py run_tests```

### API-Endpoints

#### Product Endpoints : /api/v1/product

Method | Endpoint | Functionality
--- | --- | ---
POST | /api/v1/product | Create a product
GET | /api/v1/product | Get all products
GET | /api/v1/product/productId | Get a single product

#### Sales Endpoints : /api/v1/sales

Method | Endpoint | Functionality
--- | --- | ---
POST | /api/v1/sales | Create a sales order
GET | /api/v1/sales | Get all sales orders
GET | /api/v1/sales/salesId | Get a single sales order

#### User Authentication endpoints

Method | Endpoint | Functionality
--- | --- | ---
POST | /auth/register | Register a User
POST | /auth/login | Login a user
