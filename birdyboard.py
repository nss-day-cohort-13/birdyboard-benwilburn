class Birdyboard:

    pass

    def new_user(self):

        print('Enter Full Name')

        print('Enter Username')

        print('Enter Password')

    def select_user(self):

        pass

    def sign_in(self):

        pass

    def create_public_chirp(self):

        pass

    def create_private_chrip(self):

        pass

    def view_chirps(self):

        pass

        def public_chirps(self):

            pass

        def private_chirps(self):

            pass

    def show_menu(self):

        print('1.) New User')

        print('2.) Sign In')

        print('3.) New Public Chirp')

        print('4.) New Private Chirp')

        print('5.) View Chirps')

        print('6.) Exit')

        selection = input("What do you want to do? >  ")

        if int(selection) > 0 and int(selection) < 6:

            if selection == '1':

                self.new_user()

            if selection == '2':

                sign_in()

            if selection == '3':

                create_public_chirps()

            if selection == '4':

                create_private_chirps()

            if selection == '5':

                view_all_chirps()

if __name__ == '__main__':
    birdyboard = Birdyboard()
    birdyboard.show_menu()
