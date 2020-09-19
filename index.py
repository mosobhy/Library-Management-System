from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
# import the loaduitype method which is going to allow us to use the library.ui design
from PyQt5.uic import loadUiType
import sys
# connect to the database that has been created by the Peewee orm using the sqlalchemy library.
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import os

# now let's laod the library.ui design into our script
MainUI,_ = loadUiType('library.ui')

# define the Main window class which will inhert from the main window of the library.ui
class Main(QMainWindow, MainUI):
    def __init__(self, parent = None):
        super(Main, self).__init__(parent)
        QMainWindow.__init__(self)

        self.session = {}

        self.setupUi(self)

        # call the ui_changes method.
        self.ui_changes()

        # call the method connect_db to connect to the database when instantiating an object
        self.connect_db()

        # call the button handling to operate it when the app starts.
        self.button_handling()

        # call the load categories method when the program starts.
        self.load_all_categories()

        # the rest load function that are responsible for loading the data out of the database to teh comboboxes
        self.load_tables()

        self.load_users()

        self.load_branches()

        self.load_publishers()

        self.load_authors()


    # create the functionality of the application.
    # we are going to create a method for each action can be performed on the system and connect it to the button
    
    ''' handling the UI changes happens'''
    def ui_changes(self):
        
        # make the login tab load the first.
        self.tabWidget.setCurrentIndex(0)

        # hide the upper tabBar
        self.tabWidget.tabBar().setVisible(False)


    
    ''' connnect to the database '''
    def connect_db(self):
        # create an engine using the environment variable to pass the database url
        self.engine = create_engine(os.getenv('DATABASE_URL'))
        self.db = scoped_session(sessionmaker(bind=self.engine))

        print('Database Connected Successfully!')


    ''' in this functions we are going to connect the buttons with taps '''
    def button_handling(self):
        # handling the buttons connecting with tabs
        self.pushButton_2.clicked.connect(self.open_today)
        self.pushButton.clicked.connect(self.open_books)
        self.pushButton_3.clicked.connect(self.open_clients)
        self.pushButton_5.clicked.connect(self.open_dashboard)
        self.pushButton_4.clicked.connect(self.open_history)
        self.pushButton_7.clicked.connect(self.open_reports)
        self.pushButton_6.clicked.connect(self.open_settings)

        # handling the adding data
        self.pushButton_22.clicked.connect(self.add_branch)
        self.pushButton_23.clicked.connect(self.add_author)
        self.pushButton_24.clicked.connect(self.add_publisher)
        self.pushButton_25.clicked.connect(self.add_category)

        # adding user;
        self.pushButton_30.clicked.connect(self.add_user)

        # checking user data
        self.pushButton_32.clicked.connect(self.check_user)
        # save user after edining
        self.pushButton_31.clicked.connect(self.edit_user)

    ''' lgoin tap '''
    def login(self):
        pass


    ''' daily operations tap '''
    def daily_operations(self):
        pass


    ''' Books tap '''
    def view_books(self):
        pass

    def add_book(self):
        pass

    def edit_book(self):
        pass

    def remove_book(self):
        pass

    def export_books(self):
        pass


    ''' Client tap '''
    def view_clients(self):
        pass

    def add_client(self):
        pass

    def edit_client(self):
        pass

    def remove_client(self):
        pass

    def export_clients(self):
        pass


    ''' history tap '''
    def history(self):
        pass

    
    ''' reports tap '''
    def top_books(self):
        pass

    def top_clients(self):
        pass

    def grap_monthly_report(self):
        pass



    ''' settings tap '''
    def add_branch(self):
        # access the data entered throught the lineedits
        # this is similar to flask when trying to access the data using name = request.form.get('name')
        branch_name = self.lineEdit_13.text()
        branch_code = self.lineEdit_31.text()
        branch_address = self.lineEdit_30.text()

        # insert this data into the branch table in the database.
        self.db.execute('INSERT INTO branch(code, name, address) VALUES(:var1, :var2, :var3)', 
                {
                    'var1': int(branch_code),
                    'var2': branch_name,
                    'var3': branch_address
                }
        )
        self.db.commit()
        print("------Branch Inserted Successfully------")

        # clear the lineEdit after insertion
        self.lineEdit_13.clear()
        self.lineEdit_31.clear()
        self.lineEdit_30.clear()

        # show successfully added branch
        self.statusBar().showMessage('Branch Added Successfully')


    def add_publisher(self):
        # first access the data entered throught the lineEdits.
        # this is similar to flask when trying to access the data using name = request.form.get('name')
        publisher_name = self.lineEdit_34.text()
        publisher_address = self.lineEdit_35.text()
        publisher_email = self.lineEdit_56.text()
        publisher_phone = self.lineEdit_57.text()

        # insert these data into the publisher table in the database
        self.db.execute('INSERT INTO Publisher(name, mail, phone, address) VALUES(:var1, :var2, :var3, :var4)',
            {
                'var1': publisher_name,
                'var2': publisher_email,
                'var3': publisher_phone,
                'var4': publisher_address
            }
        )
        self.db.commit()
        print("-------------Publisher Added Successfully-------------")

        # clear the lineEdit after insertion
        self.lineEdit_34.clear()
        self.lineEdit_35.clear()
        self.lineEdit_56.clear()
        self.lineEdit_57.clear()

        # show successfully added Publisher
        self.statusBar().showMessage('Publisher Added Successfully')



    def add_category(self):
        # access the data entered in the lineEdit and then insert into the database tabel category
        category_name = self.lineEdit_36.text()
        
        # access the chioce(text) select from the combobox
        parent_category = self.comboBox_11.currentText()

        # now we have the name of the parent, so we should query the database to get its id to insert it inot the db
        parent_id = self.get_parent_category_id(parent_category)

        if not parent_id:
            parent_id = 0

        # now insert the cateogry_name and the id of the selected choice into the db
        self.db.execute('INSERT INTO category(category_name, parent_category) VALUES(:var1, :var2)',
            {
                'var1': category_name,
                'var2': parent_id
            }
        )
        self.db.commit()
        
        # call the function below to instantly load the category after adding it
        self.load_all_categories()
        print('-------category added successfully----------')

        # clear the lineEdit after insertion
        self.lineEdit_36.clear()

        # show successfully added Publisher
        self.statusBar().showMessage('Category Added Successfully')


    def get_parent_category_id(self, parent):
        # this function is going to check if a parent category exist or not, if exist >>> return id
        parent_id = self.db.execute('SELECT id FROM category WHERE category_name = :var',
            {
                'var': parent
            }
        ).fetchone()

        if not parent_id:
            return False

        return parent_id.id


    def load_all_categories(self):
        # this function only purpose in life is to load the categories form the database to the parent category combobox in teh settings tab
        
        #before we load anything in the combobox, we should clear it to avoid the duplications happens due to this function called in the add_category()
        self.comboBox_11.clear()
        self.comboBox_2.clear()
        self.comboBox_7.clear()

        rows = self.db.execute('SELECT category_name FROM category').fetchall()
        if not rows:
            print('there is no categories filled yet dude ')

        # now load these fucking shits into the combobox.
        for category in rows:
            self.comboBox_11.addItem(category.category_name)
            self.comboBox_2.addItem(category.category_name)
            self.comboBox_7.addItem(category.category_name)

    
    def load_authors(self):
        
        authors = self.db.execute('SELECT name FROM author').fetchall()
        if not authors:
            print('no authors yet')

        for author in authors:
            self.comboBox_4.addItem(author.name)
            self.comboBox_5.addItem(author.name)


    def load_publishers(self):
        
        publishers = self.db.execute('SELECT name FROM publisher').fetchall()
        if not publishers:
            print('No publishers yet')

        for publisher in publishers:
            self.comboBox_3.addItem(publisher.name)
            self.comboBox_6.addItem(publisher.name)


    def load_branches(self):
        
        branches = self.db.execute('SELECT name FROM branch').fetchall()
        if not branches:
            print('No branches yet')

        for branch in branches:
            self.comboBox_18.addItem(branch.name)
            self.comboBox_13.addItem(branch.name)


    def load_users(self):
        
        users = self.db.execute('SELECT name FROM employee').fetchall()
        if not users:
            print('No Employees yet')

        for user in users:
            self.comboBox_17.addItem(user.name)


    def load_tables(self):
        
        # we could use a python list instead of this query and it will work
        tables = self.db.execute('''SELECT table_name
                            FROM information_schema.tables
                            WHERE table_schema = 'public'
                            ORDER BY table_name
                    ''').fetchall()
        
        for table in tables:
            self.comboBox_14.addItem(table.table_name)


    def add_author(self):
        # first access the data entered throught the lineEdits.
        # this is similar to flask when trying to access the data using name = request.form.get('name')
        author_name = self.lineEdit_33.text()
        author_email = self.lineEdit_32.text()
        author_phone = self.lineEdit_55.text()

        # insert this data into author table in the database
        self.db.execute('INSERT INTO Author(name, mail, phone) VALUES(:var1, :var2, :var3)',

            {
                'var1': author_name,
                'var2': author_email,
                'var3': author_phone
            }
        )
        self.db.commit()
        print('-----------Author Added Successfully------------')

        # clear the lineEdit after insertion
        self.lineEdit_33.clear()
        self.lineEdit_32.clear()
        self.lineEdit_55.clear()

        # show successfully added author
        self.statusBar().showMessage('Author Added Successfully')



    def add_user(self):
        # access the data entered throught the lineedis.
        username = self.lineEdit_40.text()
        phone = self.lineEdit_42.text()
        email = self.lineEdit_43.text()
        national_id = self.lineEdit_41.text()
        password = self.lineEdit_49.text()
        password_confirm  =self.lineEdit_48.text()

        if password == password_confirm:
            # insert the data into the database.
            self.db.execute('INSERT INTO employee(name, phone, mail, national_id, password) VALUES(:var1, :var2, :var3, :var4, :var5)',
                {
                    'var1': username,
                    'var2': phone,
                    'var3': email,
                    'var4': national_id,
                    'var5': password
                }
            )
            self.db.commit()
            print('User added Successfully')

            # clear the data from the lineEdits
            self.lineEdit_40.clear()
            self.lineEdit_42.clear()
            self.lineEdit_43.clear()
            self.lineEdit_41.clear()
            self.lineEdit_49.clear()
            self.lineEdit_48.clear()

            # show successfully added user
            self.statusBar().showMessage('User Added Successfully')

        else:
            self.statusBar().showMessage('The Password Is Not Matching')
            print('the password is not matching')
    
    def check_user(self):
        # access the data entered by the user in the lineEdit
        username = self.lineEdit_45.text()
        password = self.lineEdit_50.text()

        # check the data entered is correct or not
        check_data = self.db.execute('SELECT name, password FROM employee WHERE name = :var1 AND password = :var2',
            {
                'var1': username,
                'var2': password
            }
        ).fetchone()
        
        if not check_data:
            print('data provided is incorrect')
            self.statusBar().showMessage('Incorrect Data')
            self.lineEdit_45.clear()
            self.lineEdit_50.clear()

        else:
            # get the rest data from the database for this user and display it into the lineEdits
            data = self.db.execute('SELECT * FROM employee WHERE name = :var1 AND password = :var2',
                {
                    'var1': username,
                    'var2': password
                }
            ).fetchone()

            if not data:
                print('there is fuckning error, Line 422')

            # now display the data retrieved from the db in the lineEdits for editing it.
            self.lineEdit_44.setText(data.phone)
            self.lineEdit_47.setText(data.mail)
            self.lineEdit_46.setText(data.national_id)
            self.lineEdit_51.setText(data.password)

            self.statusBar().showMessage('Correct User!')


    def edit_user(self):
        # now after the user edit the data, we have to access it again to update it into the db
        phone = self.lineEdit_44.text()
        email = self.lineEdit_47.text()
        national_id = self.lineEdit_46.text()
        password_after_update = self.lineEdit_51.text()

        # query the db for this user id
        user_id = self.db.execute('SELECT id FROM employee WHERE national_id = :var1',
            {
                'var1': national_id
            }
        ).fetchone()
        if not user_id:
            print('error Line 453')
            self.statusBar().showMessage("Don't fuck with that fields")

        else:
            self.db.execute('''
                UPDATE employee
                SET phone = :var1,
                    mail = :var2,
                    national_id = :var3,
                    password = :var4
                WHERE
                    id = :var5
            ''',
                {
                    'var1': phone,
                    'var2': email,
                    'var3': national_id,
                    'var4': password_after_update,
                    'var5': user_id.id
                }
            )
            self.db.commit()

            print('data updated successfully')
            self.statusBar().showMessage('User Data Updated Successfully')

            # clear all the lineEdits
            # check
            self.lineEdit_45.clear()
            self.lineEdit_50.clear()

            # edit
            self.lineEdit_44.clear()
            self.lineEdit_47.clear()
            self.lineEdit_46.clear()
            self.lineEdit_51.clear()


    def permissions(self):
        pass

    def admin_reports(self):
        pass


    ''' connecting buttons with its corresponding taps '''

    def open_today(self):
        self.tabWidget.setCurrentIndex(1)

        print('today is opened')

    def open_books(self):
        self.tabWidget.setCurrentIndex(2)
        # the following line is to load the first tab in the books tab by default
        self.tabWidget_2.setCurrentIndex(0)

        print('books is opened')

    def open_clients(self):
        self.tabWidget.setCurrentIndex(3)
        # the following line is to load the first tab in the books tab by default
        self.tabWidget_3.setCurrentIndex(0)

        print('clients is opened')

    def open_dashboard(self):
        self.tabWidget.setCurrentIndex(4)

        print('dashboard is opened')


    def open_history(self):
        self.tabWidget.setCurrentIndex(5)

        print('history is opened')


    def open_reports(self):
        self.tabWidget.setCurrentIndex(6)
        # the following line is to load the first tab in the books tab by default
        self.tabWidget_5.setCurrentIndex(0)

        print('reports is opened')


    def open_settings(self):
        self.tabWidget.setCurrentIndex(7)
        # the following line is to load the first tab in the books tab by default
        self.tabWidget_4.setCurrentIndex(0)

        print('settings is opened')


'''
don't forget to convert the qrc file of the icons into a python file using the following command
    >>>pyrcc5 -o icon_rc.py icon.qrc
'''

def main():
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()



