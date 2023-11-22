import mysql.connector as sql
import time
import sys
from colorama import init, Fore, Style, Back
import pwinput as pw
import random
import re
import termtables as tt


mycon = sql.connect(host = '127.0.0.1', user = 'root', passwd = '', database = 'cbt_db')
mycursor = mycon.cursor()

# Dtatbase Creation
# mycursor.execute('CREATE DATABASE cbt_db')
# mycon.commit()

# Table Creation
# mycursor.execute('CREATE TABLE cbt_table (user_id INT(4) PRIMARY KEY AUTO_INCREMENT, lastname VARCHAR(20), firstname VARCHAR(20), middlename VARCHAR(20), user_name VARCHAR(20) UNIQUE, level VARCHAR(5), course VARCHAR(50), matric_no VARCHAR(11) UNIQUE, score FLOAT(4),percentage FLOAT(4), pWd VARCHAR(6) UNIQUE)')
# mycon.commit()

init()
class Cbt:
    def __init__(self):
        self.access()

    def access(self):
         print(f'''
                    Select one of the options:
                    1. Examiner
                    2. Student
                    0. Exit
          ''')
         var = input('Select: ')
         if var.strip() == '1':
              self.admin()
         elif var.strip() == '2':
              self.intro()
         elif var.strip() == '0':
              print(Fore.RED+'Exit'+Style.RESET_ALL)
              sys.exit()
         else:
              print(Fore.YELLOW+'Invalid Input!'+Style.RESET_ALL)
              self.access()

    def admin(self):
          self.level = input("Level: ")
          self.course = input('Course: ')  
          query = "SELECT * FROM cbt_table WHERE level=%s AND course=%s"
          val = (self.level, self.course)
          mycursor.execute(query,val)
          output = mycursor.fetchall()
          if output:
               self.course = output[0][6]
               self.level = output[0][5]
               quer = 'SELECT matric_no, lastname, firstname, middlename, score, course FROM cbt_table WHERE level=%s AND course=%s'
               var = (self.level, self.course)
               mycursor.execute(quer, var)
               rows = mycursor.fetchall()
               header = ['matric_no', 'lastname', 'firstname', 'middlename', 'score','course']
               
               print(Fore.YELLOW+"Loading..."+Style.RESET_ALL)
               time.sleep(2)
               tt.print(rows,header)
               self.max_min_score()
          else:
               print(Fore.RED+'Invalid Input!'+Style.RESET_ALL)
               print(Fore.RED+'Try Again!'+Style.RESET_ALL)
               self.admin()            
     
    def max_min_score(self):
         quer = 'SELECT MAX(score), MIN(score), course FROM cbt_table WHERE level=%s AND course=%s'
         var = (self.level, self.course)
         mycursor.execute(quer, var)
               
         print(f'''
                    THE MAXIMUM AND MINIMUM SCORES ARE FOUND THE TABLE BELLOW:
          ''')      
         rows = mycursor.fetchall()
         header = ['MAX(score)', 'MIN(score)', 'course']
         tt.print(rows,header)
         self.another_trial()

    def intro(self):
          self.reg()
          self.inq()

    def reg(self):
        self.numOfStud = []
        self.numberOfStudents = int(input("number of candidate(s): "))
        self.number = 1
        
        for val in range(self.numberOfStudents):
          print(f'CANDIDATE  NUMBER ({self.number}) IS REQUIRED TO FILL THIS, THANK YOU.')
          self.lastName = input("last name: ")
          self.firstName = input("first name: ")
          self.middleName = input("middle name: ")
          self.user = input('Username: ')
          self.matric()
          self.lvl()
          self.course = input("course: ")
          self.per = 0.0
          self.score = 0
          
          self.gen_pass = self.user
          self.name = (self.lastName.strip().capitalize(), self.firstName.strip().capitalize(), self.middleName.strip().capitalize(), self.user.strip(), self.level, self.course.strip().upper(), self.matric_no, self.score, self.per, self.gen_pass)
          self.score = 0
          val = self.numOfStud.append(self.name)
          print(self.name)
          self.que()
          self.number +=1 
   

    def que(self):
         try:
               query = 'INSERT INTO cbt_table(lastname, firstname, middlename, user_name, level, course, matric_no, score, percentage, pWd) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
               val = (self.lastName.strip().capitalize(), self.firstName.strip().capitalize(), self.middleName.strip().capitalize(), self.user.strip(), self.level, self.course.strip().upper(), self.matric_no, self.score, self.per, self.gen_pass)
               mycursor.execute(query, val)
               mycon.commit()
         except:
               print(Fore.RED+"Natric Number or Username already exits!"+Style.RESET_ALL)  
         else:
              pass
             
    def inq(self):
            print('Press ENTER to take the test or 0 to TERMINATE')
            user = input('Select: ')
            if user == '0':
                 print(Fore.RED+'TERMINATED!'+Style.RESET_ALL)
                 sys.exit()
            else:          
               self.login()

    def matric(self):
         self.matric_no = input("Matric Number: ")
         if re.match(r'^\d+$', self.matric_no):
              pass
         else:
              time.sleep(1)
              print(Fore.RED+"Matric number must be digit only"+Style.RESET_ALL)
              self.matric() 

    def lvl(self):
         self.level = input("Level: ")
         if re.match(r'^\d+$', self.level):
              pass
         else:
              time.sleep(1)
              print(Fore.RED+"Must be digit only"+Style.RESET_ALL)
              self.lvl() 

    def login(self):
         num = 1
         for i in range(self.numberOfStudents):
          print(f"""
                   CANDIDATE  NUMBER ({num}) IS REQUIRED TO LOGIN
                   THANK YOU.       
          """)
          num +=1 
          self.user = input(f'Username: ')
          self.matric_no = input(f"Matric Number: ")  
          query = 'SELECT * FROM cbt_table WHERE matric_no=%s AND user_name=%s'
          val = (self.matric_no, self.user)
          mycursor.execute(query, val)
          details = mycursor.fetchall()
          if details:
               self.last_name = details[0][1]
               self.first_name = details[0][2]
               self.other_names = details[0][3]
               user = details[0][4]
               matric_no = details[0][7]
               pwd = details[0][10]
               score = details[0][8]
               if self.user == user:
                    print(f"""
                         WELCOME TO THIS COMPUTER BASED TEST CANDIDTE NUMBEER: {self.number}
                         Hi {user}
                         
                         MATRIC NUMBER: {matric_no}
                    """)
                    self.check_pass()
                    self.question()   
               else:
                    print(Fore.RED+'Invalid Username!'+Style.RESET_ALL)
                    self.login()
          else:
                    print(Fore.RED+'Invalid Input!'+Style.RESET_ALL)
                    self.login() 

    def check_pass(self):
          self.passWord()
          pwd = pw.pwinput("Password: ") 
          if pwd == self.gen_pass:
                try:
                     query = 'UPDATE cbt_table SET pWd=%s WHERE matric_no=%s'
                     val = (pwd, self.matric_no)
                     mycursor.execute(query, val) 
                     mycon.commit()
                except:
                       print(Fore.RED+'Check Your Password!'+Style.RESET_ALL)
                       self.check_pass() 
                else:
                     pass              
          else:
               print(Fore.RED+'Invalid'+Style.RESET_ALL)
               self.check_pass()
                  
    def passWord(self):
            alpha = "abcdefghijklmnopqrstuvwxyz"
            upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            num = "123456789"
            sign = "!@#$%&()/?{]{].,'_-"

            length = 6

            res = alpha + upper + num + sign 

            self.gen_pass = "".join(random.sample(res, length))

            query = 'SELECT * FROM cbt_table WHERE matric_no=%s AND user_name=%s'
            val = (self.matric_no, self.user)
            mycursor.execute(query, val)
            details = mycursor.fetchall()
            if details:
                user = details[0][4]
                matric_no = details[0][7]
                pwd = details[0][10]
                query = 'UPDATE cbt_table SET pWd=%s WHERE matric_no=%s'
                val = (self.gen_pass, self.matric_no)
                mycursor.execute(query, val) 
                mycon.commit()
                   
            print(f"""
                    Hi {user}, your one time password is {self.gen_pass}
            """)
           
    def check_password(self):
         self.matric_no = input('Matric Number: ')
         password = pw.pwinput("Password: ")
         query = 'SELECT * FROM cbt_table WHERE pWd=%s AND matric_no=%s'
         val = (password, self.matric_no)
         mycursor.execute(query, val)
         details = mycursor.fetchall()
         if details:
              self.matric_no = details[0][6]
              self.gen_pass = details[0][9]
              
              if self.gen_pass != password:
                print(Fore.RED+'Wrong Password!'+Style.RESET_ALL)
                self.check_password()
              else:
                    pass
         else:
               print(Fore.RED+'Invalid Input!'+Style.RESET_ALL) 
               self.check_password() 

    def question(self):
            print('Fetching questions...')
            time.sleep(2)
            questions = {'TRUE':'Asiwaju Bola Ahmed Tinubu is the president of Nigeria.  True or False?',
                        'ABUJA':'Capital of Nigeria is?', 
                        'OYO':'Which state is Ibadan located?',
                        'B':'Which type of case is WORD? a.) Lower b.) Upper c.) Sentence d.) toggle', 
                        'SEYI MAKINDE':'Who is the governor of Oyo State?',
                        'IBADAN':'What is the largest city in west africa?',
                        'FRANCE':'Which country has its capital to be Paris?',
                        '6':'How many geo-political zones are in Nigeria?',
                        'UNITED STATES DOLLAR':'What is the full meaning of usD?',
                        'HEN AND RAM':'As bullock is for bull, capoon and weather(sheep) is for ______ and _______'
            }
            listing = 1
            mark = 0
            for answer, quest in questions.items():
                print('\nplease wait...') 
                time.sleep(1) 
                print(f'\n{listing}.) {quest}\n')
                
                listing +=1
                inp = input("Answer: ")
                if inp.upper().strip() == answer:
                    mark +=1
                     
            print('please wait...') 
            time.sleep(2)      
            self.mark = f'{mark} of {listing}'
            self.percentage = (mark/(listing -1))*100 
            print(f'\nDear {self.last_name} {self.first_name} {self.other_names}, you obtained {(mark)} of {listing -1}\n')                      
            self.upd()

    def upd(self):
            myquery = 'UPDATE cbt_table SET score=%s, percentage=%s WHERE matric_no=%s'
            val = (self.mark,self.percentage, self.matric_no)
            mycursor.execute(myquery, val)
            mycon.commit()   

    def another_trial(self):
         print('Press'+Fore.GREEN+' 1 '+Style.RESET_ALL+'to fetch another data or',Fore.GREEN+'0'+Style.RESET_ALL+' to Terminate')

         user = input('Select: ')
         if user == '1':
              self.admin()
         elif user == '0':
              print(Fore.RED+'Terminated!'+Style.RESET_ALL)
              sys.exit()   
         else:
              print(Fore.YELLOW+'Invalid Input!'+Style.RESET_ALL)        

cbt = Cbt()
