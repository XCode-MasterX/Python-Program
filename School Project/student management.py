import mysql.connector as msc

# GLOBAL #
con = msc.connect(user = 'root', host = 'localhost', password = input("Enter the SQL Password: "))
cur = con.cursor()
# END #

def exec(command):
    cur.execute(command)

def update_all_student_grades(connection):
    connection.cursor().execute("update students set class = class + 1;");

def create_id(student_info):
    id = str(student_info['mobile'][0:5])
    id += str(student_info['firstname'])
    student_info['student_id'] = id;

def info_to_sql(stud):
    string = ""
    for i in stud:
        if type(stud[i]) is str:
            string += f"{i} = \'{stud[i]}\', "
        elif type(stud[i]) is int:
            string += f"{i} = {stud[i]}, "
    
    return string[0 : -2]

def remove_student(id):
    exec('delete from Students where student_id = id;')

def admit_new_student():
    stud = {}
    stud['firstname'] = input('Enter the firstname of student: ')
    stud['lastname'] = input('Enter the lastname of the student')
    stud['f-name'] = input('Enter the fathers name: ')
    stud['m-name'] = input('Enter the mothers name: ')
    stud['mobile'] = input('Enter the mobile number: ')
    stud['dob'] = input('Enter the date of birth: ')
    stud['class'] = input('Enter the class of the student: ')
    stud['section'] = input('Enter the section of the student: ')
    stud['address'] = input('Enter the address: ')
    stud['pin'] = input('Enter the pin of the address: ')
    create_id(stud)
    x = info_to_sql(stud)
    exec(f'insert into values({x})')

def update_student(id):
    exec(f"select * from students where student_id = {id}")
    
    new_info = ['id', 'firstname', 'lastname', 'father_name', 'mother_name', 'mobile', 'email', 'dob', 'class', 'section', 'address', 'pin', 'fees', 'fees_paid']
    new_info = zip(new_info, cur.fetchall()[0])
    ch = int(input("What would you like to update?\n1: Mobile\n2: Email\n3: Class\n4: Section\n5: "))
    
    if ch == 1:
        new_info['mobile'] = input('Enter the new mobile number: ')
    elif ch == 2:
        new_info['email'] = input("Enter the new email: ")
    elif ch == 3:
        new_info['class'] = input("Enter the new class: ")
    elif ch == 4:
        new_info['section'] = input("Enter the new section: ")
    
    new_info = info_to_sql(new_info)
    command = f"update Students set {new_info} where student_id = {id}"
    exec(command)

def pay_fees(id):
    fee = int(input("Enter the amount paid: "))
    exec(f'update Student set fees = fees + {fee} where student_id = {id}')

def check_database_existance():
    exec('show databases;')
    databases = [i[0] for i in cur.fetchall()]
    if 'institution' not in databases:
        exec("create database Institution;")
    exec('use Institution;');

def display_students():
    exec('select * from Students')
    output = cur.fetchall()
    for i in output:
        print(*i)

def check_table_existance():
    exec('use Institution;')
    exec('show tables;')
    if cur.fetchall() == []:
        exec('''create table Students
                (student_id varchar(10) PRIMARY KEY,
                firstname varchar(15) NOT NULL,
                lastname varchar(15) NOT NULL,
                father_name varchar(30),
                mother_name varchar(30),
                mobile char(10) NOT NULL,
                email varchar(50),
                date_of_birth date NOT NULL,
                class varchar(5) NOT NULL,
                section varchar(2) NOT NULL,
                address varchar(50) NOT NULL,
                pin varchar(10) NOT NULL,
                fees integer,
                fees_paid integer);''')

def main():
    pass

if __name__ == "__main__":
    check_database_existance()
    check_table_existance()
    password = "12345"
    for i in range(5):
        enter_pass = input("Enter the password: ")
        if enter_pass == password:
            break
        else:
            print(f"Wrong password. {5-i-1} chances left.")
    else:
        from sys import exit
        exit()
    
    main() # TODO