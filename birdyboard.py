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

    Main menu. Prints intial menu and prompts for a selection.

    Selection is then passed to the runner function

    '''
    global users_directory
    global current_user
    global public_chirps_directory
    global private_chirps_directory
    global conversations_directory

    clear_menu()
    if current_user:
        print('Current User: ' + current_user.user_name)

    print('\n1.) New User')
    print('\n2.) Select User')
    print('\n3.) New Chirp')
    print('\n4.) View Chirps')
    print('\n5.) Exit')

    selection = input("\nWhat do you want to do? >  ")

    if int(selection) > 0 and int(selection) < 6:

        runner(selection)

    else:

        show_menu()

#############################################################################
############################# 3. Runner Methods #############################
#############################################################################

def runner(selection):
    '''

    This function accepts a single argument, selection.

    Runner takes selection and checks for matches to the main menu numbers,
    then it calls the corresponding function.

    Method Arguments:
    ----------------
    selection = a varible containing user input from the main menu function

    '''

    clear_menu()

    if selection == '1':

        run_create_user()

    if selection == '2':

        run_select_user()

    if selection == '3':

        run_chirp_creator()

    if selection == '4':

        run_view_all_chirps()

def run_create_user():
    '''

    Creates instance of a user.

    This function creates a new user and assigns it to a variable,
    then it sets current user to that variable.

    '''

    global current_user

    clear_menu()

    # sets created user to variable
    user = create_new_user()

    # sets current_user to user object just created
    current_user = user

    clear_menu()
    show_menu()

def run_select_user():
    '''

    This function calls the print users function and sets the return value of
    that function to a variable.

    That variable is passed into the select user function which returns a
    user object.

    Finally, current user is set to return value of select user.

    '''

    global current_user

    clear_menu()

    # puts all users in a list
    stored_users_list = print_users()

    # sets current user to input selected user object
    current_user = select_user(stored_users_list)

    show_menu()

def run_chirp_creator():
    '''

    This function prompts user for a public chirp.

    If user input is yes it runs a helper function called,
    run public create chirp.

    If user input is no it runs another helper function called,
    run private create chirp.

    '''
    global public_chirps_directory
    global private_chirps_directory
    global conversations_directory

    clear_menu()
    decision = input('\npublic chirp? (y/n) > ')

    if decision.lower()[0] == 'y':

        run_create_public_chirp()

    if decision.lower()[0] == 'n':

        run_create_private_chirp()

def run_view_all_chirps():
    '''

    This function prints a sub menu to either view public or private chirps,
    and then prompts the user for a choice.

    If user selects '1' and havent yet signed in, they will still be able to
    see all public chirps, but they won't be able to reply.

    If user select 1 and have signed in, they will be able to see all public
    chirps and be given an option to reply.

    If user selects 2 and haven't signed in, they will be rerouted back to
    the choices.

    If user selects 2 and has signed in, they will will be shown private chirps
    between them and others. But only if their Id is attached to the chirp,
    either as an author or a recipient

    If user selects 3, they are rerouted back to the main menu

    If user selects anything else, they are shown the sub menu again.

    '''
    global public_chirps_directory
    global private_chirps_directory
    global conversations_directory

    clear_menu()

    # prints sub menu for viewing all chirps
    print('1.) View Public Chirps')
    print('\n2.) View Private Chirps')
    print('\n3.) Exit')
    choice = input('\nWhich chirps do you want to see? > ')


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

    if choice < '1' or choice > '3':
        clear_menu()
        input('Oopsie, you entered an invalid number, press ENTER to continue')
        run_view_all_chirps()

def run_create_public_chirp():
    '''

    Calls create public chirp function

    Serialize function serializes public chirps directory to public chirps file.

    If the new public chirp is not already a conversation, it creates a new
    conversation.

    '''
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
    '''

    Calls create private chirp function

    Serialize function serializes private chirps directory to private chirps
    file.

    If the new private chirp is not already a conversation, it creates a new
    conversation.

    '''

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
    '''

    Prompts user for message input.

    Creates new instance of public chirp and passes in current user id
    and message from the user input.

    '''
    global current_user

    message = input('\nWat r u chirping? > ')

    # creates new instance of a public chirp with current user id and message
    new_chirpy = Chirp(current_user.obj_id, message)

    return new_chirpy

def view_all_public_chirps():
    '''

    Puts all public chirp objects into a list.

    Gets the length of the list and adds 1 for the exit option.

    Prints chirp message from each public chirp object in the list.

    Returns the length of the list

    '''
    global public_chirps_directory

    # creates list holding all chirp objects in public chirps directory
    public_chirps = list(public_chirps_directory.values())

    # get the number of chirp objects in public chirps directory ## for exit menu option
    public_chirps_length = len(public_chirps) + 1


    # prints all public chirp messages from chirp objects in public chirps directory
    print('\nAll Public Chirps: ')
    [print('\n' + str(index) + '.) ' + value.chirp_message) for index, value in enumerate(public_chirps, start=1)]
    print('\n' + str(public_chirps_length) + '.) Exit')

    return public_chirps_length



def no_user_show_public_chirps():
    '''

    Runs View All Public Chirps.

    Then, runs make user sign in. Either create user or select user.

    '''
    global public_chirps_directory

    view_all_public_chirps()
    reroute = input('\nMust sign in to reply, press ENTER to continue > ')
    make_user_sign_in()

def show_public_chirps_to_current_user():
    '''

    Creates a list containing public chirp objects from the public chirps
    directory.

    Prints all public chirps via view all public chirps

    Prompts if user wants to reply.

    If user wants to reply, calls create_new_chirp function.

    Calls get public reply chirps and sets its return value to a variable,
    which is a list of replies within a conversation.

    Then appends the new chirp to the conversation replies list with the chirp id
    as the key and the chirp object as the value and serializes the public
    chirps directory to the public chirps file.

    '''
    global public_chirps_directory
    global conversations_directory

    public_chirps = list(public_chirps_directory.values())
    public_chirps_length = view_all_public_chirps()
    selection = int(input('\nchirp back? (enter number) > '))

    if selection < public_chirps_length and selection > 0:

        # sets targetId to chirp_id they want to reply to
        targetId = public_chirps[(int(selection) - 1)].obj_id
        conversation = get_public_reply_chirps(targetId)
        to_reply = input('\ndo you want to reply(y/n) > ')

        if to_reply.lower()[0] == 'y':

            reply_chirp = create_public_chirp()
            conversation.append({reply_chirp.obj_id: reply_chirp})
            serialize_data(conversations_directory, 'conversations.txt')
            run_view_all_chirps()

        else:

            run_view_all_chirps()

    else:

        run_view_all_chirps()

def get_public_reply_chirps(targetId):
    '''
    If target id is equal to the chirp id property on a conversation, it sets
    a variable equal to the list of replies on the same conversation.

    If target id is not equal to the chirp id property, it says 'no replies'.

    If the conversation does exist, it prints all replies in the replies list
    property on the conversation.

    Method Arguments:
    -----------------

    targetId = chirp selected from public chirps list

    '''
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
            print('No replies')

        else:
            print('\nreplies:')

            # checks all replys within the conversation object reply list
            for reply in conversation:

                # prints all messages in conversation object reply list
                for data in reply.values():
                    print('\n ' + data.chirp_message)

        # return the matched converation
        return conversation

def make_user_sign_in():
    '''

    Makes user choose wether or not to create a new user select an existing
    user or exit to the main menu. (Called if user looks at public chirps and
    wants to reply)

    '''
    clear_menu()

    print('1.) Create User')
    print('\n2.) Select User')
    print('\n3.) Exit')
    selection = input('\nwhat do you want to do? (enter number) > ')

    if selection == '1':

        run_create_user()

    if selection == '2':

        run_select_user()

    if selection == '3':

        show_menu()

#############################################################################
######################## 5. Private Chirp  Methods ##########################
#############################################################################

def create_private_chirp():
    '''

    Prompts user for message input.

    Creates new instance of private chirp and passes in current user id,
    message from the user input, and a recipient selected from choose_target
    function.

    '''
    global current_user

    message = input('\nWat r u chirping? > ')

    # selects who current user wants to chirp to
    recipient = choose_target()

    # creates new instance of private chirp with current user and recipient id and message
    new_chirpy = Chirp(current_user.obj_id, message, recipient.obj_id)

    return new_chirpy

def view_all_private_chirps():
    '''

    Puts all private chirp objects into a list.

    Gets the length of the list and adds 1 for the exit option.

    Prints chirp message from each private chirp object in the list.

    Returns the length of the list

    '''
    global private_chirps_directory

    # creates a list of all chirp objects in private chirps directory
    private_chirps = list(private_chirps_directory.values())

    # get the number of chirp objects in private chirps directory ## for exit menu option
    private_chirps_length = len(private_chirps) + 1

    # prints all private chirp messages from chirp objects in private chirps directory
    print('All Private Chirps: ')
    [print('\n' + str(index + 1) + '.) ' + value.chirp_message) for index, value in enumerate(private_chirps)]
    print('\n' + str(private_chirps_length) + '.) Exit')

    return private_chirps_length

def no_user_reroute():
    '''
    Reroutes user to a menu where he has to choose to create a new user, select
    from an existing user or exit to the main menu. (Used when user tries to get
    into private chirps)
    '''
    clear_menu()

    input('\nMust be logged in to see private chirps, press ENTER to continue')
    make_user_sign_in()

def show_private_chirps_to_current_user():
    '''

    Creates a list containing private chirp objects from the private chirps
    directory.

    Checks if the current user id ==

    Prints all private chirps via view all private chirps

    Prompts if user wants to reply.

    If user wants to reply, calls create_new_chirp function.

    Calls get private reply chirps and sets its return value to a variable,
    which is a list of replies within a conversation.

    Then appends the new chirp to the conversation replies list with the chirp id
    as the key and the chirp object as the value and serializes private chirps
    directory to the private chirps file.

    '''
    global private_chirps_directory
    global conversations_directory

    private_chirps = list(private_chirps_directory.values())
    for chirps in private_chirps_directory.values():
        if chirps.author == current_user.obj_id or chirps.recipient == current_user.obj_id:
            private_chirps_length = view_all_private_chirps()
            selection = int(input('\nchirp back? (enter number) > '))

            if selection < private_chirps_length and selection > 0:

                targetId = private_chirps[(int(selection) - 1)].obj_id
                conversation = get_private_reply_chirps(targetId)
                to_reply = input('\ndo you want to reply(y/n) > ')

                if to_reply.lower()[0] == 'y':

                    reply_chirp = create_public_chirp()
                    conversation.append({reply_chirp.obj_id: reply_chirp})
                    serialize_data(conversations_directory, 'conversations.txt')
                    run_view_all_chirps()

                else:
                    run_view_all_chirps()

            else:

                clear_menu()
                input('\nPlease enter a valid number, press ENTER to continue')
                run_view_all_chirps()
        else:

            clear_menu()
            input('\nYou have no private messages at this time, press ENTER to continue')
            run_view_all_chirps()

def get_private_reply_chirps(targetId):
    '''
    If target id is equal to the chirp id property on a conversation, it sets
    a variable equal to the list of replies on the same conversation.

    If target id is not equal to the chirp id property, it says 'no replies'.

    If the conversation does exist, it prints all replies in the replies list
    property on the conversation.

    Method Arguments:
    -----------------

    targetId = chirp selected from private chirps list

    '''
    global conversations_directory
    global private_chirps_directory
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

        else:
            input('\nYou do not have any private chirps, press ENTER to continue')
            run_view_all_chirps()

        # print replies if available
        if not conversation or len(conversation) == 0:
            print('\nNo chirps')

        else:
            print('\nreplies:')

            # checks all replys within the conversation object reply list
            for reply in conversation:

                # prints all messages in conversation object reply list
                for data in reply.values():
                    print('\n ' + data.chirp_message)

        # return the matched converation
        return conversation

#############################################################################
############################# 6. General Methods ############################
#############################################################################

def get_original_selected_chirp(targetId):
    '''

    Gets the original chirp from either the public or private directory
    the users selected to reply to and prints it before the reply chirps.

    Method Arguments:
    -----------------

    targetId = the chirp the user selected to reply to

    '''
    if targetId in public_chirps_directory.keys():
        # finds target chirp and displays it
        for original_chirps in public_chirps_directory.values():

            # if chirp user selected is in public chirps directory print it
            if targetId == original_chirps.obj_id:
                print('\nOriginal Chirp:')
                print('\n ' + original_chirps.chirp_message)

    if targetId in private_chirps_directory.keys():
        # finds target chirp and displays it
        for original_chirps in private_chirps_directory.values():

            # if chirp user selected is in public chirps directory print it
            if targetId == original_chirps.obj_id:
                print('\nOriginal Chirp:')
                print('\n ' + original_chirps.chirp_message)

def serialize_data(directory, file_name, item=None):
    '''

    Method Arguments:
    -----------------
    directory = directory that needs to be serialize_data.
    file_name = name of file that is being serialized to.
    item = optional variable for if an object needs to be created in the directory
           or not.

    '''
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

    user_input = int(input('\n> '))
    stored_users_length = len(stored_users_list) + 1

    if user_input == stored_users_length:

        select_user()

    if user_input > 0 and user_input < stored_users_length:

        # searches stored user list for input selection
        user = stored_users_list[user_input - 1]
        return user

    else:

        print('Please enter a valid number')
        select_user()

def print_users():
    '''

    Creates a list of user objects from users directory.

    Gets the length of the list for the exit option.

    Prints all username within each user object in the users directory.

    '''
    global users_directory

    # creates a list holding all user objects from user_directory
    stored_users = list(user_directory.values())

    # length of the stored users list ## for printing exit in the menu
    stored_users_length = len(stored_users) + 1

    # prints usernames from all user objects in stored_users
    print('\nSelect User:')
    [print('\n' + str(index) + '.) ' + value.user_name) for index, value in enumerate(stored_users, start=1)]
    print('\n' + str(stored_users_length) + '.) Exit')

    return stored_users

def choose_target():
    '''

    This function Prints all users to be selected from and sets the return value
    from print users to a variable.

    Passes the variable into select user and then sets the return value of
    select user to current user.

    '''
    stored_users_list = print_users()
    user = select_user(stored_users_list)
    return user

def clear_menu():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

#############################################################################
########################## 8. Conversation Method ###########################
#############################################################################

def generate_new_thread(chirp_id, private):
    '''

    Creates a new instance of a conversation and passes in the chirp id from
    the newly created chirp and wether or not the conversation is private or not.

    Method Arguments:
    -----------------
    chirp_id = Id of the chirp that is being used to generate a new conversation.
    private = Either a true or false value (boolean)

    '''
    global conversations_directory

    # creates new instance of conversation object
    new_convo = Conversation(chirp_id, private)

    # serializes conversations directory now holding newly created conversation object
    serialize_data(conversations_directory, 'conversations.txt', new_convo)

if __name__ == '__main__':
    show_menu()
