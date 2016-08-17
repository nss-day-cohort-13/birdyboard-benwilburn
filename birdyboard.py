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
private_chirps_directory = serialization.deserialize('private_chirps.txt')
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

            selection = input('public chirp? (y/n) > ')
            if selection == 'y' or selection == 'Y' or selection == 'yes' or selection == 'Yes':
                new_public_chirp = create_public_chirp()
                if new_public_chirp.obj_id not in public_chirps_directory:
                    try:
                        generate_new_thread(new_public_chirp.obj_id, False)
                    except TypeError:
                        print(error)

                view_all_public_chirps()
            if selection == 'n' or selection == 'N' or selection == 'no' or selection == 'No':
                new_private_chirp = create_private_chirp()
                if new_private_chirp.obj_id not in private_chirps_directory:
                    try:
                        generate_new_thread(new_private_chirp.obj_id, True)
                    except TypeError:
                        print(error)
                view_all_private_chirps()

        if selection == '4':
            print('1. View Public Chirps')
            print('2. View Private Chirps')
            choice = input('Which chirps do you want to see? > ')
            if choice == '1':
                view_all_public_chirps()
            if choice == '2':
                view_all_private_chirps()

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

def create_public_chirp():
    global current_user
    global user_directory
    global public_chirps_directory

    message = input('Wat r u chirping? > ')
    new_chirpy = Chirp(current_user.obj_id, message)
    public_chirps_directory[new_chirpy.obj_id] = new_chirpy
    serialization.serialize('public_chirps.txt', public_chirps_directory)
    return new_chirpy


def create_private_chirp():
    global current_user
    global user_directory
    global private_chrips_directory

    message = input('Wat r u chirping? > ')
    recipient = select_user()
    new_chirpy = Chirp(current_user.obj_id, message, recipient.obj_id)
    private_chirps_directory[new_chirpy.obj_id] = new_chirpy
    serialization.serialize('private_chirps.txt', private_chirps_directory)
    return new_chirpy

def view_all_public_chirps():
    global public_chirps_directory
    global conversations_directory

    print('All Public Chirps: ')
    public_chirps = list(public_chirps_directory.values())
    public_chirps_length = str(len(public_chirps) + 1)
    [print(str(index + 1) + '. ' + value.chirp_message) for index, value in enumerate(public_chirps)]
    print(public_chirps_length + '. Exit')
    reply = input('chirp back? (enter number) > ')
    if reply < str(public_chirps_length):
        target = public_chirps[(int(reply) - 1)].obj_id
        for item in conversations_directory.keys():
            print('hey')
            print(item)
    else:
        show_menu()

def view_all_private_chirps():
    global private_chirps_directory
    global conversations_directory

    print('All Private Chirps: ')
    private_chirps = list(private_chirps_directory.values())
    [print(str(index + 1) + '. ' + value.chirp_message) for index, value in enumerate(private_chirps)]

def generate_new_thread(chirp_id, private):
    global conversations_directory

    new_convo = Conversation(chirp_id, private)
    conversations_directory[new_convo.obj_id] = new_convo
    serialization.serialize('conversations.txt', conversation_directory)

d

if __name__ == '__main__':
    show_menu()
