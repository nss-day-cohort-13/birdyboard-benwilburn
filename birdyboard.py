import uuid
import pickle
import serialization
from chirp import *
from user import *
from conversation import *

class Birdyboard:

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

                print('Enter Full Name')
                fullname = input('fullname >  ')
                print('Enter Username')
                username = input('username >  ')


            if selection == '2':

                select_user()

            if selection == '3':


                create_public_chirps()

            if selection == '4':

                create_private_chirps()

            if selection == '5':

                view_all_chirps()

if __name__ == '__main__':
    birdyboard = Birdyboard()
    birdyboard.initial_menu()
