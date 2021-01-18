# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 16:28:06 2020

@author: 00ery
"""

#Login System - Project 1:
import time

#asking whether login or signup
valid = False
while valid == False:
    mode = input("Would you like to log in or sign up? (1=Log in, 0=Sign up): \n")
    if mode == '1' or mode == '0':
        valid = True
    else:
        print("Please enter a 1 or a 0")

#opening file contents as dictionary
def load():
    users_dict = {}
    with open('users.txt', 'r') as db:
        for line in db.readlines():
            x = line.split()
            if x != []:
                users_dict[x[0]] = x[1]
            else:
                continue
    return users_dict

#saving dictionary into file
def save(user_data):
    with open('users.txt', 'w') as db:
        db.truncate()
        for key in user_data:
            user = key+' '+user_data[key]+'\n'
            db.write(user)

db = load()  
  
#logging in        
if mode == '1':
    print("------Logging in:------ \n")
    valid_un = False
    while valid_un == False:
        user_name = input('Please enter username: \n')
        if user_name in db:
            valid_un = True
        else:
            print("Username not recognised. \n")
            
    valid_pw = False
    while valid_pw == False:
        pass_word = input('Please enter password: \n')
        if pass_word in db.values():
            valid_pw = True
            print("You have successfully logged in. \n")
            time.sleep(2)
        else:
            print("Password not recognised: \n")

#signing up
else:
    #obtaining new username
    print("------Signing up:------ \n")
    valid_nun = False
    while valid_nun == False:
        new_user_name = input("Please enter a username: \n")
        if new_user_name in db:
            print("Username taken. \n")
        else:
            valid_nun = True
    #obtaining new password
    valid_npw = False
    while valid_npw == False: 
        new_pass_word_1 = input("Please enter a password: \n")
        new_pass_word_2 = input("Please confirm password: \n")
        if new_pass_word_1 == new_pass_word_2:
            print("You have successfully created a new account. \n")
            db[new_user_name] = new_pass_word_1
            save(db)
            time.sleep(5)
            valid_npw = True
        else:
            print("Passwords do not match. \n")
            
            
        
        
                

        
    
    
    

    

    
   