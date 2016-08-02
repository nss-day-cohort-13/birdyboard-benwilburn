class Birdyboard:
    pass

    def new_user(self):
        print('Enter Full Name')
        print('Enter Username')
        print('Enter Password')

    def select_user(self):
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
        print('3.) Public Chirp')
        print('4.) Private Chirp')
        print('5.) View Chirps')
        print('6.) Exit')

if __name__ == '__main__':
    birdyboard = Birdyboard()
    birdyboard.show_menu()
