# here i am working on a desktop application so, i am gonna use the peewee library which supports the ORM for desktop
# instead of using sqlalchemy which not supporting the desktop apps.
from peewee import *
from datetime import datetime


# configure and connect to the database.
db = PostgresqlDatabase('library', user='mosobhy', host='localhost', password='123')

book_status = (
    (1, 'New'),
    (2, 'Old'),
    (3, 'Damedged')
)

class Category(Model):
    category_name = CharField(unique=True)
    parent_category = IntegerField(null=True)      # recursive relationship

    class Meta:
        database = db

class Author(Model):
    name = CharField()
    mail = CharField(null=True, unique=True)
    phone = CharField(max_length=11, unique=True)

    class Meta:
        database = db

class Publisher(Model):
    name = CharField(unique=True)
    mail = CharField(null=True, unique=True)
    phone = CharField(max_length=11)
    address = CharField(null=True)

    class Meta:
        database = db


# design the database layout and tables and all relations right below using the peewee Model class
class Book(Model):
    # (null = False) == (NOT NULL)  and the null=Flase is the default 
    code = CharField(max_length=20, unique=True)
    title = CharField(max_length=200, unique=True)   # the max length specify the maximum amount of charactrs to be inserted in this column
    # the ForeignKeyField() method specifys the relation between tables such as references in sql
    # the first parameter in it is the table name to be related with.
    # the order of classes does not matter in the peewee librarys
    author = ForeignKeyField(Author, backref='author', null=True)
    publisher = ForeignKeyField(Publisher, backref='publisher', null=True)
    category = ForeignKeyField(Category, backref='category', null=True)
    description = TextField(null=True)
    status = CharField(choices=book_status) # choices is an optional parameter which takes a tuple of tuples ((value, 'display'), (value2, 'display2))
    price = DecimalField(null=True)
    image = CharField(null=True)     # i am gonna store the images of the books in a folder and put the path of that folder in teh database.

    class Meta:
        database = db



class Client(Model):
    name = CharField()
    phone = CharField(max_length=11, unique=True)
    mail = CharField(null=True, unique=True)
    national_id = CharField(max_length=14, null=True, unique=True)

    class Meta:
        database = db


class Branch(Model):
    code = IntegerField(null=True, unique=True)
    name = CharField()
    address = CharField(null=True)

    class Meta:
        database = db

class Employee(Model):
    name = CharField()
    phone = CharField(max_length=11, unique=True)
    mail = CharField()
    national_id = CharField(max_length=14, unique=True)
    password = CharField(max_length=100)

    class Meta:
        database = db

tables = (
    (1, 'Book'),
    (2, 'Client'),
    (3, 'Category'),
    (4, 'Author'),
    (5, 'Publisher'),
    (6, 'Branch'),
    (7, 'Empolyee'),
    (8, 'History'),
    (9, 'Daily Movements')
)

operations = (
    (1, 'Login'),
    (2, 'Update'),
    (3, 'Create'),
    (4, 'Delete')
)

class History(Model):
    branch = ForeignKeyField(Branch, backref='branch')
    employee = ForeignKeyField(Employee, backref='user')
    action = CharField(choices=operations)      # choices
    table = CharField(choices=tables)        # choices
    date = DateTimeField(default=datetime.now())

    class Meta:
        database = db

transaction = (
    (1, 'Borrow'),
    (2, 'Return')
)

class Daily_movements(Model):
    branch = ForeignKeyField(Branch, backref='branch', null=True)
    employee = ForeignKeyField(Employee, backref='user', null=True)
    book = ForeignKeyField(Book, backref='book')
    client = ForeignKeyField(Client, backref='client')
    transaction_type = CharField(choices=transaction)      # ['borrow', 'return']
    time_from = DateTimeField(null=True)
    time_to = DateTimeField(null=True)
        
    class Meta:
        database = db

# connect to the database and create all tables and relations
db.connect()
db.create_tables([Book, Client, Category, Author, Publisher, Branch, Employee, History, Daily_movements])

