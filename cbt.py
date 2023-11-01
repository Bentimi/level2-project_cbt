import mysql.connector as sql
import time
import sys
from colorama import init, Fore, Style
import pwinput as pw
import random

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
        # self.reg()
        self.reg()
    def reg(self):
        self.numOfStud = []
        self.numberOfStudents = int(input("number of candidate(s): "))
        self.number = 1
        
        for val in range(self.numberOfStudents):
          #   if val == self.numberOfStudents:
          print(f'CANDIDATE  NUMBER ({self.number}) IS REQUIRED TO FILL THIS, THANK YOU.')
          self.lastName = input("last name: ")
          self.firstName = input("first name: ")
          self.middleName = input("middle name: ")
          self.user = input('Username: ')
          self.matric_no = int(input("matric number: "))
          self.level = int(input("level: "))
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
     #    else:
     #      print('Hey!!!')
   

    def que(self):
         try:
               query = 'INSERT INTO cbt_table(lastname, firstname, middlename, user_name, level, course, matric_no, score, percentage, pWd) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
               val = (self.lastName.strip().capitalize(), self.firstName.strip().capitalize(), self.middleName.strip().capitalize(), self.user.strip(), self.level, self.course.strip().upper(), self.matric_no, self.score, self.per, self.gen_pass)
               mycursor.execute(query, val)
               mycon.commit()
         except:
          print(Fore.RED+"Natric Number or Username already exits!"+Style.RESET_ALL)  
         else:
               self.inq()
             
               


    def inq(self):
            print('Press ENTER to take the test or 0 to TERMINATE')
            user = input('Select: ')
            if user == '0':
                 print(Fore.RED+'TERMINATED!'+Style.RESET_ALL)
                 sys.exit()
            else:          
               self.login()


    def login(self):
         self.user = input('Username: ')
         self.matric_no = input("Matric Number: ")  
         query = 'SELECT * FROM cbt_table WHERE matric_no=%s AND user_name=%s'
         val = (self.matric_no, self.user)
         mycursor.execute(query, val)
         details = mycursor.fetchall()
         if details:
          #     last_name = details[0][1]
          #     first_name = details[0][2]
          #     other_names = details[0][3]
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
               # self.question()    
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
            num = "1234567890"
            sign = "!@#$%&*_-"

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
               #  self.question()

                print(Fore.RED+'Wrong Password!'+Style.RESET_ALL)
                self.check_password()
              else:
                    pass
         else:
               print(Fore.RED+'Invalid Input!'+Style.RESET_ALL) 
               self.check_password()             

    def upd(self):
            myquery = 'UPDATE cbt_table SET score=%s, percentage=%s WHERE matric_no=%s'
            val = (self.mark,self.percentage, self.matric_no)
            mycursor.execute(myquery, val)
            mycon.commit()   

cbt = Cbt()