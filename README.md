# Store Manager

[![Build Status](https://travis-ci.com/waracci/store-manager-v2.svg?branch=master)](https://travis-ci.com/waracci/store-manager-v2)
[![Coverage Status](https://coveralls.io/repos/github/waracci/store-manager-v2/badge.svg?branch=ft-auth-product-sales-endpoints-161431065)](https://coveralls.io/github/waracci/store-manager-v2?branch=ft-auth-product-sales-endpoints-161431065)
[![Maintainability](https://api.codeclimate.com/v1/badges/cbaff03d141b6cd93d47/maintainability)](https://codeclimate.com/github/waracci/store-manager-v2/maintainability)

## Introduction

Store Manager is a web application that helps store owners manage sales and product inventory records. This application is meant for use in a single store.

### Features

1. Admin can add a product.
2. Admin/store attendant can get all products
3. Admin/store attendant can get a specific product
4. Store attendant can add a sale order
5. Admin can get all sale records
6. Admin can manage addition, editing and deletion of categories

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

#### Product Endpoints : /api/v2/product

Method | Endpoint | Functionality
--- | --- | ---
POST        | /api/v2/product                       | Create a product
GET         | /api/v2/product                       | Get all products
GET         | /api/v2/product/productId             | Get a single product
PUT         | /api/v2/product/productId             | Edit a single product
Delete      | /api/v2/product/productId             | Delete a product

#### Sales Endpoints : /api/v2/sales

Method | Endpoint | Functionality
--- | --- | ---
POST            | /api/v2/sales             | Create a sales order
GET             | /api/v2/sales             | Get all sales orders
GET             | /api/v2/sales/salesId     | Get a single sales order
Delete          | /api/v2/sales/saleId      | Delete a sales record

#### User Authentication endpoints

Method | Endpoint | Functionality
--- | --- | ---
POST                | /api/v2/auth/register         | Register a User
POST                | /api/v2/auth/login            | Login a user
POST                | /api/v2/auth/logout           | Logout a user

#### Category Endpoints : /api/v2/category

Method | Endpoint | Functionality
--- | --- | ---
POST        | /api/v2/category                        | Create a category
GET         | /api/v2/category                        | Get all categories
GET         | /api/v2/category/categoryId             | Get a single category
PUT         | /api/v2/category/categoryId             | Edit a single category
Delete      | /api/v2/category/categoryId             | Delete a category
