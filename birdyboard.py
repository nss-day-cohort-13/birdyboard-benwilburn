import uuid
import pickle
import collections
import serialization
import os
from chirp import *
from user import *
from conversation import *

####################################
#######       Index          #######
####################################
##     1. Global Values           ##
##     2. Menu Method             ##
##     3. Runner Methods          ##
##     4. Public Chirp Methods    ##
##     5. Private Chirp Methods   ##
##     6. General Methods         ##
##     7. User Methods            ##
##     8. Conversation Method     ##
####################################

#############################################################################
############################# 1.Global Values ###############################
#############################################################################

# all directorys = dictionary
user_directory = serialization.deserialize('users.txt')
public_chirps_directory = serialization.deserialize('public_chirps.txt')
private_chirps_directory = serialization.deserialize('private_chirps.txt')
conversations_directory = serialization.deserialize('conversations.txt')
current_user = None

#############################################################################
############################# 2. Menu Method ################################
#############################################################################

def show_menu():
    '''
    Main menu. This is where everything connects
    '''
    global users_directory
    global current_user
    global public_chirps_directory
    global private_chirps_directory
    global conversations_directory

    if current_user:
        print('Current User: ' + current_user.user_name)

    print('1.) New User')
    print('2.) Select User')
    print('3.) New Chirp')
    print('4.) View Chirps')
    print('5.) Exit')

    selection = input("What do you want to do? >  ")

    if int(selection) > 0 and int(selection) < 6:

        runner(selection)

    else:

        show_menu()

#############################################################################
############################# 3. Runner Methods #############################
#############################################################################

def runner(selection):

    if selection == '1':

        run_create_user()

    if selection == '2':

        run_select_user()

    if selection == '3':

        run_chirp_creator()

    if selection == '4':

        run_view_all_chirps()


def run_create_user():
    global current_user

    # sets created user to variable
    user = create_new_user()

    # sets current_user to user object just created
    current_user = user

    show_menu()

def run_select_user():
    global current_user

    # puts all users in a list
    stored_users_list = print_users()

    # sets current user to input selected user object
    current_user = select_user(stored_users_list)

    show_menu()

def run_chirp_creator():
    global public_chirps_directory
    global private_chirps_directory
    global conversations_directory

    decision = input('public chirp? (y/n) > ')

    if decision.lower()[0] == 'y':

        run_create_public_chirp()

    if decision.lower()[0] == 'n':

        run_create_private_chirp()

def run_view_all_chirps():
    global public_chirps_directory
    global private_chirps_directory
    global conversations_directory

    # prints sub menu for viewing all chirps
    print('1. View Public Chirps')
    print('2. View Private Chirps')
    print('3. Exit')
    choice = input('Which chirps do you want to see? > ')


    if choice == '1' and current_user == None:

        no_user_show_public_chirps()

    if choice =='1' and current_user != None:

        show_public_chirps_to_current_user()

    if choice == '2' and current_user == None:

        no_user_reroute()

    if choice == '2' and current_user != None:

        show_private_chirps_to_current_user()

    if choice == '3':

        show_menu()

def run_create_public_chirp():
    # creates new instance of a public chirp and assigns it to a variable
    new_public_chirp = create_public_chirp()

    # creates new public chirp object in public chirps directory and serializes it
    serialize_data(public_chirps_directory, 'public_chirps.txt', new_public_chirp)

    # if new_public_chirp isn't in conversations directory, it creates new conversation
    if new_public_chirp.obj_id not in conversations_directory:

        try:

            generate_new_thread(new_public_chirp.obj_id, False)

        except TypeError:

            print(error)

    show_menu()

def run_create_private_chirp():
    # creates new instance of a private chirp and assigns it to a variable
    new_private_chirp = create_private_chirp()

    # creates new private chirp object in private chirps directory and serializes it
    serialize_data(private_chirps_directory, 'private_chirps.txt', new_private_chirp)

    # if new_private_chirp isn't in conversations directory, it creates new conversation
    if new_private_chirp.obj_id not in conversations_directory:

        try:

            generate_new_thread(new_private_chirp.obj_id, True)

        except TypeError:

            print(error)

    show_menu()


#############################################################################
######################### 4. Public Chirp Methods ###########################
#############################################################################

def create_public_chirp():
    global current_user

    message = input('Wat r u chirping? > ')

    # creates new instance of a public chirp with current user id and message
    new_chirpy = Chirp(current_user.obj_id, message)

    return new_chirpy

def view_all_public_chirps():
    global public_chirps_directory

    # creates list holding all chirp objects in public chirps directory
    public_chirps = list(public_chirps_directory.values())

    # get the number of chirp objects in public chirps directory ## for exit menu option
    public_chirps_length = len(public_chirps) + 1


    # prints all public chirp messages from chirp objects in public chirps directory
    print('All Public Chirps: ')
    [print(str(index) + '. ' + value.chirp_message) for index, value in enumerate(public_chirps, start=1)]
    print(str(public_chirps_length) + '. Exit')

    return public_chirps_length

def no_user_show_public_chirps():
    global public_chirps_directory

    public_chirps = list(public_chirps_directory.values())
    public_chirps_length = view_all_public_chirps()
    reroute = input('Must sign in to reply, press ENTER to continue > ')
    make_user_sign_in()

def show_public_chirps_to_current_user():
    global public_chirps_directory
    global conversations_directory

    public_chirps = list(public_chirps_directory.values())
    public_chirps_length = view_all_public_chirps()
    selection = int(input('chirp back? (enter number) > '))

    if selection < public_chirps_length and selection > 0:

        targetId = public_chirps[(int(selection) - 1)].obj_id
        conversation = get_reply_chirps(targetId)
        to_reply = input('do you want to reply(y/n) > ')

        if to_reply.lower()[0] == 'y':

            reply_chirp = create_public_chirp()
            conversation.append({reply_chirp.obj_id: reply_chirp})
            serialize_data(conversations_directory, 'conversations.txt')
            run_view_all_chirps()

        else:

            run_view_all_chirps()

    else:

        run_view_all_chirps()

def make_user_sign_in():
    print('1. Create User')
    print('\n2. Select User')
    print('\n3. Exit')
    selection = input('what do you want to do? (enter number) > ')

    if selection == '1':

        run_create_user()

    if selection == '2':

        run_select_user()

    if selection == '3':

        show_menu()

#############################################################################
######################## 5. Private Chirp  Mehtods ##########################
#############################################################################

def create_private_chirp():
    global current_user

    message = input('Wat r u chirping? > ')

    # selects who current user wants to chirp to
    recipient = select_user()

    # creates new instance of private chirp with current user and recipient id and message
    new_chirpy = Chirp(current_user.obj_id, message, recipient.obj_id)

    return new_chirpy

def view_all_private_chirps():
    global private_chirps_directory

    # creates a list of all chirp objects in private chirps directory
    private_chirps = list(private_chirps_directory.values())

    # get the number of chirp objects in private chirps directory ## for exit menu option
    private_chirps_length = len(private_chirps) + 1

    # prints all private chirp messages from chirp objects in private chirps directory
    print('All Private Chirps: ')
    [print(str(index + 1) + '. ' + value.chirp_message) for index, value in enumerate(private_chirps)]
    print(str(private_chirps_length) + '. Exit')

    return private_chirps_length

def no_user_reroute():

    input('Must be logged in to see private chirps')
    show_menu()


#############################################################################
############################# 6. General Methods ############################
#############################################################################

def get_reply_chirps(targetId):
    global conversations_directory
    global public_chirps_directory
    global user_directory
    global current_user

    conversation = None
    # find conversation that contains the target chrip
    for conversation_id, conversation_data in conversations_directory.items():

        # checks to see if chirp user selected is in the conversations directory
        if targetId == conversation_data.chirp_id:

            # sets conversation to be list of replies in the conversation object
            conversation = conversation_data.replies

            get_original_selected_chirp(targetId)

        # print replies if available
        if not conversation or len(conversation) == 0:
            print('No chirps')

        else:
            print('\nreplies:')

            # checks all replys within the conversation object reply list
            for reply in conversation:

                # prints all messages in conversation object reply list
                for data in reply.values():
                    print('\n ' + data.chirp_message)

        # return the matched converation
        return conversation

def get_original_selected_chirp(targetId):
    # finds target chirp and displays it
    for original_chirps in public_chirps_directory.values():

        # if chirp user selected is in public chirps directory print it
        if targetId == original_chirps.obj_id:
            print('Original Chirp:')
            print('\n ' + original_chirps.chirp_message)

def serialize_data(directory, file_name, item=None):

    # if item exists create new object (key = item.obj_id, value = item) in directory
    if item != None:
        directory[item.obj_id] = item

    # serializes specified directory into specified file
    serialization.serialize(file_name, directory)

#############################################################################
############################# 7. User Methods ###############################
#############################################################################
def create_new_user():
    '''
    Creates a new user

    Method Arguments:
    -----------------
    n/a
    '''
    global user_directory

    print('Enter Full Name')
    fullname = input('fullname >  ')
    print('Enter Username')
    username = input('username >  ')
    # creates instance of user with inputs
    user = User(fullname, username)
    # serializes user_directory containing newly created user
    serialize_data(user_directory, 'users.txt', user)
    return user

def select_user(stored_users_list):
    '''
    Selects user based on user input based on the print_users method

    Method Arguments:
    -----------------

    stored_users_list = A list of all user Ids
    '''

    user_input = int(input('\n > '))

    # searches stored user list for input selection
    user = stored_users_list[user_input - 1]

    return user

def print_users():
    global users_directory

    # creates a list holding all user objects from user_directory
    stored_users = list(user_directory.values())

    # length of the stored users list ## for printing exit in the menu
    stored_users_length = len(stored_users) + 1

    # prints usernames from all user objects in stored_users
    print('Select User:')
    [print(str(index) + '. ' + value.user_name) for index, value in enumerate(stored_users, start=1)]
    print(str(stored_users_length) + '. Exit')

    return stored_users

#############################################################################
########################## 8. Conversation Method ###########################
#############################################################################

def generate_new_thread(chirp_id, private):
    global conversations_directory

    # creates new instance of conversation object
    new_convo = Conversation(chirp_id, private)

    # serializes conversations directory now holding newly created conversation object
    serialize_data(conversations_directory, 'conversations.txt', new_convo)

if __name__ == '__main__':
    show_menu()
