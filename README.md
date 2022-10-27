# splitwise
Backend Clone of famous Splitwise App

## Local Setup

1. Install python = 3.9.13

2. Install postgres

3. After cloning the repo

  ```
  pip install -r requirements
  ```
  
4. create .env file in root directory, and create subsequent DB, user, password in postgres
  ```
  DB_NAME='sample_db'
  DB_USER='sample_user'
  DB_PASSWORD='sample_pass'
  ```

5. (For Running unittests) Assign permission to DB_USER to create DB
  ```
  ALTER USER myuser CREATEDB;
  ```
  
  ```
  python manage.py test
  ```
  

6. Run the server
  ```
  python manage.py runserver
  ```



Features

C-Create, R-Read, U-Update, D-Delete

The R of group shows who-owes-who in group, and R of user shows who-owes-who in all groups having that user

1. CR User, Cant UD User, Cant change global Balance
2. CR Group (Automatically creates unknown users inside them), U Group(if the deleted users have pending money in PayMap, cant U), D(if any pending money, cant D)
3. CRUD Expense (Rebalance on the group and global level)


## API Collection
