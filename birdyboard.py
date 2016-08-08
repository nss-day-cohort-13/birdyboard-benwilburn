import uuid
import pickle
import collections
import serialization
from chirp import *
from user import *
from conversation import *

class Birdyboard:

    def __init__(self):

        self.users_directory = list()
        self.public_chirps = list()
        self.private_chirps = list()
        self.current_user = None

    def initial_menu(self):

        print('1.) New User')

        print('2.) Select User')

        print('3.) New Public Chirp')

        print('4.) New Private Chirp')

        print('5.) View Chirps')

        print('6.) Exit')

        selection = input("What do you want to do? >  ")

        if int(selection) > 0 and int(selection) < 6:

            if selection == '1':

                counter = 1

                print('Enter Full Name')
                fullname = input('fullname >  ')
                print('Enter Username')
                username = input('username >  ')
                user_codex = User(fullname, username)
                self.users_directory.append(user_codex)
                print('users', self.users_directory)
                serialization.serialize('users.txt', self.users_directory)
                self.current_user = username
                show_menu()

            if selection == '2':

                select_user()
                show_menu()

            if selection == '3':

                create_public_chirp()

            if selection == '4':

                create_private_chirp()

            if selection == '5':

                view_all_chirps()

    def show_menu(self):

        print('1.) New Public Chirp')

        print('2.) New Private Chirp')

        print('3.) View Chirps')

        print('4.) Exit')

        selection = input("What do you want to do? >  ")

        if selection == '1':

            create_public_chirp()

        if selection == '2':

            create_private_chirp()

        if selection == '3':

            view_all_chirps()

if __name__ == '__main__':
    birdyboard = Birdyboard()
    birdyboard.initial_menu()
