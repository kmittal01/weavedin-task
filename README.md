#### Installation Steps: ####
* Create new Virtual Environment
* install requirements by:
```bash
pip insall -r requirements.txt
```
* Create database in mysql and update DB_URL in app/config/base.py
* Migrate Database to create table by:
```bash
python manage.py db migrate
```
* Run the python server by using the following command:
```bash
python manage.py runserver
```
* In a separate terminal, run Tests by the following command:
```bash
py.test
```
* The tests will create a new token, a new user, two new items and one variants of each. The test will also run update commands on variants and items, during which, 
update_transaction_logs will also be generated into the db. 
The test will also call the apis to `get transaction update logs` of the current user,
and for all the users.


* In order to test apis from postman, a new user has to be created first and 
then the token is required to be fetched. The process is self-explanatory in the tests/ module.

#### Future Work ####

* The APIs performance can be improved by using bulk_create methods, instead of using loops.
* The text of the notifications can be improved.