#!/usr/bin/env python3
import sys
import os
import argparse
import random
import datetime 


def usage():
    print("calculator by Jonas, Uni Potsdam, 2020")
    print("Usage: calculator --arg value")
    exit()


# write out color constants
#
# SGR color constants
# rene-d 2018

class Colors:
    """ ANSI color codes """
    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BROWN = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    LIGHT_GRAY = "\033[0;37m"
    DARK_GRAY = "\033[1;30m"
    LIGHT_RED = "\033[1;31m"
    LIGHT_GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    LIGHT_BLUE = "\033[1;34m"
    LIGHT_PURPLE = "\033[1;35m"
    LIGHT_CYAN = "\033[1;36m"
    LIGHT_WHITE = "\033[1;37m"
    BOLD = "\033[1m"
    FAINT = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    NEGATIVE = "\033[7m"
    CROSSED = "\033[9m"
    END = "\033[0m"


def color_text(text, col):
    """Function to color text according to the ANSI codes."""
    col_text: str = getattr(Colors, col) + text + getattr(Colors, 'END')

    return col_text


class Calculator():
    ''' Class implementing the calculator functionality.
    '''
    def __init__(self, score_correct = 3, score_deduct = -1):
        self.n_problems = 1
        self.score = 0
        self.exc_score = 0
        self.n_exercise = 0
        self.score_correct = score_correct
        self.score_deduct = score_deduct
        self.points_per_second = 0
        # lookup for which exercise name corresponds to each exercise function. 
        # Should be updated when extending the class or inheriting from it.
        self.exercise_options = {'addition': 'add_exercise()', 'multiplication': 'multi_exercise()'}

        self.hs_filename = 'highscores.tab'
        self.res_filename = 'results.tab'

        # generate the name lookup for short exercise names
        self._generateOptNameLookup()
            
    def _generateOptNameLookup(self):
        ''' Method to generate a lookup dict for the long option and the short option. This will
        however get messy as soon as we have exercise names with non unique first characters.
        Maybe then we need to start using ids or something. Should be called after changing
        things in the exercise_options dict.
        '''

        self.exercise_options_lookup = {opt[0]:opt for opt in self.exercise_options.keys()} 
        
    def _getUserName(self):
        self.user = input('Type your name and press enter to confirm...\n')

    def exercise(self, lower, upper, sign):
        """ Function for letting the user do a generic maths exercise 
        involing two random numers with an upper and lower bound. 
        Keeps score.
        """

        # always reset exercise score at the start
        self.exc_score = 0

        # generate two random numbers
        num_1 = random.randint(lower, upper)
        num_2 = random.randint(lower, upper)

        # get sum of both numbers. Solution will be coerced to string for later comparison.
        corr_sol = str(eval(f'{num_1} {sign} {num_2}'))

        # ask user for solution.
        print('Here is your problem. Please enter the solution:')
        user_sol = input(f'\t{num_1} {sign} {num_2} = ')

        while True:
            if user_sol == 'q':  # user want's to leave

                print('Sorry to see you go. Have a nice day!')

                break

            elif user_sol != corr_sol:  # user is wrong

                print(color_text('WRONG!\n', 'RED'))
                print('Try again!')

                user_sol = input(f'\t{num_1} {sign} {num_2} = ')

                # deduct from score
                self.exc_score += self.score_deduct

            elif user_sol == corr_sol:  # user is correct

                print(color_text('That is correct!', 'GREEN'))

                # increment score
                self.exc_score += self.score_correct

                # mark exercise as done
                self.n_exercise += 1

                break

        # add excercise score to global score
        self.score += self.exc_score

        # save exercise results
        self.write_results()


    def add_exercise(self, lower = 10, upper = 200):
        """ Function to let the user do an addition exercise.
        Passes on the score of the exercise.
        """

        self.task = 'a'

        self.exercise(lower, upper, '+')


    def multi_exercise(self, lower = 2, upper = 14):
        """ Function to let user do a multiplication exercise.
        Passes on the score.
        """

        self.task = 'm'

        self.exercise(lower, upper, '*')
        
        
    def write_results(self):
        """ Write results of one task into a file. """ 
        res_file = open(self.res_filename, mode = 'a')

        # get values in a list
        print_list = [str(datetime.datetime.today()), str(self.user), str(self.exc_score), str(self.task)]

        # separate values by tabs and write to the file
        res_file.write('\t'.join(print_list) + '\n')
            
        res_file.close()

    def hs_file_init(self):
        ''' Check if highscores file is present, if not create it. '''

        if not os.path.isfile('highscores.tab'):
            hs_file = open(self.hs_filename, mode = 'w')

            write_list = ['time', 'name', 'score', 'points_per_minute']

            hs_file.write('\t'.join(write_list) + '\n')

    
    def write_highscore(self):
        ''' Write points per second into file.
        ''' 

        self.hs_file_init()

        hs_file = open(self.hs_filename, mode = 'a')

        # get values in a list
        print_list = [str(datetime.datetime.today()), str(self.user), str(self.score), str(self.points_per_second)]

        # separate values by tabs and write to the file
        hs_file.write('\t'.join(print_list) + '\n')

                   
        hs_file.close()

    def check_highscores(self):
        ''' Look up current highscore in the highscore file.
        Currently works with reading lines of the file, but in 
        the furture a more robust method might be desirable.
        '''

        self.hs_file_init()

        hs_file = open(self.hs_filename)

        max_score = 0
        max_ppm = 0

        for line in hs_file:
            line_list = line.split('\t')

            if not line_list[0] == 'time':                    

                if max_score < int(line_list[2]):
                    max_score = int(line_list[2])

                if max_ppm < float(line_list[3]):
                    max_ppm = float(line_list[3])

        if self.score > max_score:
            print(color_text('That\'s a new highscore!', 'YELLOW'))

        if self.points_per_second > max_ppm:
            print(color_text('No one was this fast before!!', 'YELLOW')) 


    def do_exercise(self, only = ''):
        """Function for selecting an exercise. Saves the score achieved in each exercise and 
        passes on the score.
        """        

        # if we haven't given anything as an only value
        if not only:
            while True:
                # generate exercise selection string
                exercise_str = ''
                for l_ex in self.exercise_options.keys():
                    exercise_str = exercise_str + f'-\"{l_ex[0]}\" for {l_ex.capitalize()}\n'

                print('What do you want to do?\nType:')
                choice = input(exercise_str).strip().lower()[0]    

                print(f"You entered {choice}!")      

                if choice == 'q':  # user chooses to leave

                    print('Ok back to main menu!')
                    
                    break

                # check if the choice is a valid option
                elif choice in self.exercise_options_lookup.keys():

                    break

                else:

                    print('That was not an option. Please choose again!')
                    
                    continue
        
        else: 
            choice = only.strip().lower()[0]

        # convert choice back to long option (again, only works as long as first character of 
        # operation name is unique)
        choice = self.exercise_options_lookup[choice]

        print(f"Your choice is now {choice}! Therefore {self.exercise_options[choice]} will be called.")

        # call the exercise function corresponding to the choice
        eval('self.' + self.exercise_options[choice])


    def menu(self, n_problems = 5, only = ''):
        """ Function generating a rudimentary menu.
        User enters their name and can choose between different kinds of 
        exercise. Also keeps track of the score and announces it when the 
        user leaves.
        """

        # record starting time
        start_time = datetime.datetime.now()

        self.n_problems = n_problems

        # check if only option is a valid exercise type
        if only:
            if only not in self.exercise_options.values() and only not in self.exercise_options.keys():
                raise Exception("Option given for singular exercise type not a valid exercise type.")
    
        print(f'We\'re doing {self.n_problems} exercises today!')
        print('You can always type "q" to quit...')

        print('But first: What is your name?')
        self._getUserName()

        
        for i in range(0,self.n_problems):

            # if were further in than the first loop
            if i > 0:
                    
                # ask user if they want to continue
                user_confirm = input(f'We did {self.n_exercise} exercises so far.\nContinue?\n(Press enter or type "q" to quit)')

                # exit if user types anything
                if user_confirm != '':
                    break

            self.do_exercise(only)            

        # record stop time and get seconds since start
        stop_time = datetime.datetime.now()
        tot_time = (stop_time - start_time).total_seconds()

        self.points_per_second = self.score / tot_time
           
        print(f'You did {self.n_exercise} exercise(s)!')

        if self.score > 2:
            print(f'You managed to get {self.score} points! Congratulations!')
        elif 0 < self.score <= 2:
            print(f'You only got {self.score} point(s)? Surely you can do better!')
        elif self.score < 0:
            print(f'You have {self.score} points? You managed to become negative? Come on, try again and get better!')
        else:
            print(f'You scored {self.score} points.')

        # if more than 10 exercises were performed do the highscore interactions
        if self.n_exercise >= 10:
            self.check_highscores()
            self.write_highscore()      


class ExtendedCalculator(Calculator):
    ''' Class extending the Calculator class with additional functionality.
    for now it adds a new exercise type: subtraction.
    ''' 

    def __init__(self, score_correct = 3, score_deduct = -1):
        super().__init__(score_correct, score_deduct)
        self.exercise_options['subtraction'] = 'sub_exercise()'

        self._generateOptNameLookup()

       
    def sub_exercise(self, lower = 20, upper = 200):
        ''' Function wrapping around exercise() to implement subtraction exercises.
        '''

        self.task = 's'

        self.exercise(lower, upper, '-')



def main(args):

    # extract arguments
    # I am very proud of the n_problems part, which i did so
    #  i wont have to import math for the floor function
    # Careful, that part is utter bullshit
    only_exercise = args['only'].lower().strip()
    n_problems = abs(args['nexercises'])


    calc = ExtendedCalculator()
    calc.menu(n_problems, only_exercise)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description = 'Solve mathematical exercises!')
    parser.add_argument('-n','--nexercises',
        help = 'Specify how many exercises you want to do.',
        default = "5",
        required = False,
        type = int)
    parser.add_argument('-o','--only',
        help = 'Specify whether to only use one type of exercise.\n Either (a)ddition, (m)ultiplication or (s)ubtraction.',
        default = '',
        required = False,
        type = str)

    args = vars(parser.parse_args())
   
    main(args)
