import mysql.connector as msc

'''
TODO:
i) Admiting new student (done)
ii) Deleting Student (done)
iii) Displaying all students (done)
iv) Report of Student (not done)
v) Detail Modification (done)
vi) Fees Collection (done)
'''

# GLOBAL #
con = msc.connect(user = 'root', host = 'localhost', password = input("Enter the SQL Password: "))
cur = con.cursor()
# END #

def exec(command):
    cur.execute(command)

def update_all_student_classes(connection):
    connection.cursor().execute("update students set class = class + 1;");

def create_id(student_info):
    exec('select * from Students;')
    id = int(cur.fetchall()[0][0])
    student_info['student_id'] = id + 1

def info_to_sql(stud):
    string = ""
    for i in stud:
        if i == 'date_of_birth':
            string += f"str_to_date(\'{stud[i]}\', '%Y-%m-%d'), "
        elif type(stud[i]) is str:
            string += f"\'{stud[i]}\', "
        elif type(stud[i]) is int:
            string += f"{stud[i]}, "
    
    return string[0 : -2]

def remove_student():
    ch = int(input('\n\n1: Use ID to delete specific student\n2: Delete Students of specific Class\n3: Delete Students of specific class and section\nEnter your choice: '))
    if ch == 1:
        id = int(input("Enter the Student id you want to delete: "))
        exec(f'delete from Students where student_id = {id};')
    elif ch == 2:
        std = int(input('Enter the student class in roman-numerals: '))
        exec(f'delete from Students where class = {std};')
    elif ch == 3:
        std = int(input("Enter the students' class in roman-numerals: "))
        sec = int(input("Enter the students' section: "))
        exec(f'delete from Students where class = {std} and section = {sec};')

def admit_new_student():
    stud = {}
    create_id(stud)
    stud['firstname'] = input('Enter the firstname of student: ')
    stud['lastname'] = input('Enter the lastname of the student: ')
    stud['father_name'] = input('Enter the fathers name: ')
    stud['mother_name'] = input('Enter the mothers name: ')
    stud['mobile'] = input('Enter the mobile number: ')
    stud['email'] = input("Enter the email of the student: ")
    stud['date_of_birth'] = input('Enter the date of birth (YYYY-MM-DD): ')
    stud['class'] = input('Enter the class of the student: ')
    stud['section'] = input('Enter the section of the student: ')
    stud['address'] = input('Enter the address: ')
    stud['pin'] = input('Enter the pin of the address: ')
    stud['fee'] = input('Enter the fee of the Student: ')
    stud['fees_paid'] = input("Enter the fees paid of the student: ")
    x = info_to_sql(stud)
    print('\n\n', x, '\n\n')
    exec(f'insert into Students values({x})')

def modify_student(id):
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
    exec(f'update Student set fees_paid = fees_paid + {fee} where student_id = {id}')

def check_database_existance():
    exec('show databases;')
    databases = [i[0] for i in cur.fetchall()]
    if 'institution' not in databases:
        exec("create database Institution;")
    exec('use Institution;');

def display_students():
    exec('select * from Students;')
    output = cur.fetchall()
    for i in output:
        print(*i, sep = ' | ')

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

def student_report():
    pass

def main():
    ch = 1
    while ch != 0:
        ch = int(input("What would you like to do?\n1: Add Student\n2: Modify Student details\n3: Delete Student record\n4: Fees Collection\n5: Report of Students\n6: Display all Students\n0: Exit"))
        if ch == 1:
            admit_new_student()
        elif ch == 2:
            modify_student(int(input("\nEnter the id of the student: ")))
        elif ch == 3:
            remove_student()
        elif ch == 4:
            pay_fees(int(input("\nEnter the id of the student: ")))
        elif ch == 5:
            student_report()
        elif ch == 6:
            display_students()
        con.commit()

if __name__ == "__main__":
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

    check_database_existance()
    check_table_existance()
    main() #TODO