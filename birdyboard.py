import uuid
import pickle
import collections
import serialization
import os
from chirp import *
from user import *
from conversation import *

user_directory = serialization.deserialize('users.txt')
public_chirps_directory = serialization.deserialize('public_chirps.txt')
public_chirps_directory = serialization.deserialize('private_chirps.txt')
conversations_directory = serialization.deserialize('conversations.txt')
current_user = None

def show_menu():
    global users_directory
    global current_user
    if current_user:
        print('Current User: ' + current_user.user_name)

    print('1.) New User')

    print('2.) Select User')

    print('3.) New Chirp')

    print('4.) View Chirps')

    print('5.) Exit')

    selection = input("What do you want to do? >  ")

    if int(selection) > 0 and int(selection) < 6:

        if selection == '1':

            counter = 1

            print('Enter Full Name')
            fullname = input('fullname >  ')
            print('Enter Username')
            username = input('username >  ')
            user = User(fullname, username)
            user_directory[user.obj_id] = user
            serialization.serialize('users.txt', user_directory)
            current_user = user
            show_menu()

        if selection == '2':

            current_user = select_user()
            show_menu()

        if selection == '3':

            create_chirp()
            show_menu()

        if selection == '4':

            view_all_chirps()

def select_user():
    global current_user
    global user_directory

    stored_users_list = list()
    print('Select User:')
    for key, user_id in enumerate(user_directory):
        user = user_directory[user_id]
        stored_users_list.append(user.obj_id)
        print('\n {0}. {1}'.format(key + 1, user.user_name))
    user_input = int(input('\n > '))
    user = user_directory[stored_users_list[user_input - 1]]
    return user

def create_new_chirp():
    selection = input('public chirp? (y/n) > ')
    if selection == 'y' or selection == 'Y' or selection == 'yes' or selection == 'Yes':
        create_public_chrip()
    else:
        create_private_chirp()

def create_public_chirp():
    global current_user
    global user_directory
    global public_chirps_directory

    message = input('Wat r u chirping? > ')
    new_chirpy = Chirp(current_user.obj_id, message, False)
    public_chirps_directory[new_chirpy.obj_id] = new_chirpy
    new_convo = Conversation(new_chirpy.obj_id)
    conversation_directory[new_convo.obj_id] = new_convo
    serialization.serialize('conversations.txt', conversation_directory)

def create_private_chrip():
    global current_user
    global user_directory
    global private_chrips_directory

    message = input('Wat r u chirping? > ')
    recipient = select_user()
    new_chirpy = Chirp(current_user.obj_id, message, True, recipient)
    private_chirps_directory[new_chirpy.obj_id] = new_chirpy
    new_convo = Conversation(new_chirpy.obj_id)
    conversation_directory[new_convo.obj_id] = new_convo
    serialization.serialize('conversations.txt', conversation_directory)




if __name__ == '__main__':
    show_menu()
