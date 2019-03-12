# Name: Jade Garisch
# Email: jadeng@brandeis.edu
# Last updated: February 7, 2019
# Program: soundex.py - this program uses the soundex algorithm and 3 finite state transducers
# to convert names into their soundex form

from fst import FST
import string, sys
from fsmutils import compose

#create lists that will be used in multiple methods
alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
         'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

nums = ['1', '2', '3', '4', '5', '6']

def letters_to_numbers():
    """
    Returns an FST that converts letters to numbers as specified by
    the soundex algorithm
    """
    # Let's define our first FST (first fst)
    f1 = FST('soundex-generate')

    # conversions
    group0 = ['a', 'e', 'h', 'i', 'o', 'u', 'w', 'y', 'A', 'E', 'H', 'I', 'O', 'U', 'W', 'Y']
    group1 = ['b', 'f', 'p', 'v', 'B', 'F', 'P', 'V']
    group2 = ['c', 'g', 'j', 'k', 'q', 's', 'x', 'z', 'C', 'G', 'J', 'K', 'Q', 'S', 'X', 'Z']
    group3 = ['d', 't', 'D', 'T']
    group4 = ['l', 'L']
    group5 = ['m', 'n', 'M', 'N']
    group6 = ['r', 'R']

    # FST states
    f1.add_state('start')
    f1.add_state('1')
    f1.add_state('2')
    f1.add_state('3')
    f1.add_state('4')
    f1.add_state('5')
    f1.add_state('6')
    f1.add_state('7')

    # Indicate that 'start' is the initial state
    f1.initial_state = 'start'

    # Set the final states
    f1.set_final('1')
    f1.set_final('2')
    f1.set_final('3')
    f1.set_final('4')
    f1.set_final('5')
    f1.set_final('6')
    f1.set_final('7')

    #add remaining arcs
    for letter in string.ascii_letters:
          if letter in group0:
                f1.add_arc('start', '1', letter, letter)
          elif letter in group1:
                f1.add_arc('start','2', letter, letter)
          elif letter in group2:
                f1.add_arc('start','3', letter, letter)
          elif letter in group3:
              f1.add_arc('start', '4', letter, letter)
          elif letter in group4:
                f1.add_arc('start', '5', letter, letter)
          elif letter in group5:
                f1.add_arc('start', '6', letter, letter)
          elif letter in group6:
                f1.add_arc('start', '7', letter, letter)
          else:
                f1.add_arc('start', '1', letter, letter)
          if letter in group0:
                f1.add_arc('1', '1', letter, '')
                f1.add_arc('2', '1', letter, '')
                f1.add_arc('3', '1', letter, '')
                f1.add_arc('4', '1', letter, '')
                f1.add_arc('5', '1', letter, '')
                f1.add_arc('6', '1', letter, '')
                f1.add_arc('7', '1', letter, '')
          elif letter in group1:
                f1.add_arc('1', '2', letter, '1')
                f1.add_arc('2', '2', letter, '')
                f1.add_arc('3', '2', letter, '1')
                f1.add_arc('4', '2', letter, '1')
                f1.add_arc('5', '2', letter, '1')
                f1.add_arc('6', '2', letter, '1')
                f1.add_arc('7', '2', letter, '1')
          elif letter in group2:
                f1.add_arc('1', '3', letter, '2')
                f1.add_arc('2', '3', letter, '2')
                f1.add_arc('3', '3', letter, '')
                f1.add_arc('4', '3', letter, '2')
                f1.add_arc('5', '3', letter, '2')
                f1.add_arc('6', '3', letter, '2')
                f1.add_arc('7', '3', letter, '2')
          elif letter in group3:
                f1.add_arc('1', '4', letter, '3')
                f1.add_arc('2', '4', letter, '3')
                f1.add_arc('3', '4', letter, '3')
                f1.add_arc('4', '4', letter, '')
                f1.add_arc('5', '4', letter, '3')
                f1.add_arc('6', '4', letter, '3')
                f1.add_arc('7', '4', letter, '3')
          elif letter in group4:
                f1.add_arc('1', '5', letter, '4')
                f1.add_arc('2', '5', letter, '4')
                f1.add_arc('3', '5', letter, '4')
                f1.add_arc('4', '5', letter, '4')
                f1.add_arc('5', '5', letter, '')
                f1.add_arc('6', '5', letter, '4')
                f1.add_arc('7', '5', letter, '4')
          elif letter in group5:
                f1.add_arc('1', '6', letter, '5')
                f1.add_arc('2', '6', letter, '5')
                f1.add_arc('3', '6', letter, '5')
                f1.add_arc('4', '6', letter, '5')
                f1.add_arc('5', '6', letter, '5')
                f1.add_arc('6', '6', letter, '')
                f1.add_arc('7', '6', letter, '5')
          elif letter in group6:
                f1.add_arc('1', '7', letter, '6')
                f1.add_arc('2', '7', letter, '6')
                f1.add_arc('3', '7', letter, '6')
                f1.add_arc('4', '7', letter, '6')
                f1.add_arc('5', '7', letter, '6')
                f1.add_arc('6', '7', letter, '6')
                f1.add_arc('7', '7', letter, '')
    return f1

def truncate_to_three_digits():
    """
    Create an FST that will truncate a soundex string to three digits
    """
    # Ok so now let's do the second FST, the one that will truncate
    # the number of digself, label=None, is_final=False,
    #               finalizing_string=(), descr=Noneits to 3

    f2 = FST('soundex-truncate')

    # Indicate initial and final states
    # Indicate that 'start' is the initial state
    f2.add_state('start')
    f2.initial_state = 'start'
    f2.add_state('1')
    f2.add_state('2')
    f2.add_state('3')
    f2.add_state('4')

    #set final states
    f2.set_final('start')
    f2.set_final('1')
    f2.set_final('2')
    f2.set_final('3')
    f2.set_final('4')

    #add arcs
    for char in string.ascii_letters:
        if char.lower() in alpha:
            f2.add_arc('start', 'start', char, char)
    for num in string.digits:
        if num in nums:
            f2.add_arc('start', '1', num, num)
            f2.add_arc('1', '2', num, num)
            f2.add_arc('2', '3', num, num)
            f2.add_arc('3', '4', num, '')
            f2.add_arc('4', '4', num, '')
    return f2


def add_zero_padding():
    # Now, the third fst - the zero-padding fst
    f3 = FST('soundex-padzero')

    # Indicate initial and final states
    # Indicate that 'start' is the initial state
    f3.add_state('start')
    f3.initial_state = 'start'
    f3.add_state('1')
    f3.add_state('2')
    f3.add_state('3')
    f3.add_state('4')

    # set final states
    f3.set_final('4')

    for char in string.ascii_letters:
        if char.lower() in alpha:
            f3.add_arc('start', 'start', char, char)
    for num in string.digits:
        if num in nums:
            f3.add_arc('start', '1', num, num)
            f3.add_arc('1', '2', num, num)
            f3.add_arc('2', '3', num, num)

    f3.add_arc('start', '4', '', '000')
    f3.add_arc('1', '4', '', '00')
    f3.add_arc('2', '4', '', '0')
    f3.add_arc('3', '4', '', '')
    return f3


def soundex_convert(name_string):
    """Combine the three FSTs above and use it to convert a name into a Soundex"""
    f1 = letters_to_numbers()
    f2 = truncate_to_three_digits()
    f3 = add_zero_padding()
    word = "".join(f1.transduce(name_string)[0])
    next = "".join(f2.transduce(word)[0])
    final = "".join(f3.transduce(next)[0])
    return final

if __name__ == '__main__':
    # for Python 2, change input() to raw_input()
    user_input = input().strip()


    if user_input:
        print("%s -> %s" % (user_input, soundex_convert(list(user_input))))
