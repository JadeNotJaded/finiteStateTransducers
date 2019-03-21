# Name: Jade Garisch
# Email: jadeng@brandeis.edu
# Last updated: February 7, 2019
# Program: morphology.py - this program uses two finite state transducers to either convert words into
# their present and past form or define them as "past form" and "present participle form"

from fst import FST

class Parser():

    def generate(self, analysis):
        """Generate the morphologically correct word

        e.g.
        p = Parser()
        analysis = ['p','a','n','i','c','+past form']
        p.generate(analysis)
        ---> 'panicked'
        """

        # Let's define our first FST
        f1 = FST('morphology-generate')

        #now let's add some states
        f1.add_state('start')
        f1.add_state('1')
        f1.add_state('2')
        f1.add_state('3')
        f1.add_state('4')
        f1.add_state('5')
        f1.add_state('6')

        #now let's define our start and end state
        f1.initial_state = 'start'
        f1.set_final('6')

        for item in analysis:
            if item == 'w' or item == 'W':
                f1.add_arc('start', '1', item, item)
            elif item == 's' or item == 'S':
                f1.add_arc('start', '2', item, item)
            elif item == 'p' or item == 'P':
                f1.add_arc('start', '3', item, item)
            elif item == 'h' or item == 'H':
                f1.add_arc('start', '4', item, item)
            elif item == 'l' or item == 'L':
                f1.add_arc('start', '5', item, item)
            elif item == '+past form':
                f1.add_arc('1', '6', item, 'ed')
                f1.add_arc('2', '6', item, 'ed')
                f1.add_arc('3', '6', item, 'ked')
                f1.add_arc('4', '6', item, 'ked')
                f1.add_arc('5', '6', item, 'ed')
            elif item == '+present form':
                f1.add_arc('1', '6', item, 'ing')
                f1.add_arc('2', '6', item, 'ing')
                f1.add_arc('3', '6', item, 'king')
                f1.add_arc('4', '6', item, 'king')
                f1.add_arc('5', '6', item, 'ing')
            else:
                f1.add_arc('1', '1', item, item)
                f1.add_arc('2', '2', item, item)
                f1.add_arc('3', '3', item, item)
                f1.add_arc('4', '4', item, item)
                f1.add_arc('5', '5', item, item)

        output = (f1.transduce(analysis)[0])
        return "".join(output)

    def parse(self, word):
        """Parse a word morphologically

        e.g.
        p = Parser()
        word = ['p','a','n','i','c','k','i','n','g']
        p.parse(word)
        ---> 'panic+present participle form'
        """
        valid_words = [list('synced'), list('syncing'), list('panicked'), list('panicking'), list('licked'),
                       list('licking'), list('havocked'), list('havocking'), list('wanted'), list('wanting')]

        if word not in valid_words:
            return "Please input a valid word: synced, syncing, panicked, panicking, licked, " \
                   "licking, havocked, havocking, wanted or wanting"


        # Ok so now let's do the second FST
        f2 = FST('morphology-parse')

        # now let's add some states
        f2.add_state('start')
        f2.add_state('1')
        f2.add_state('2')
        f2.add_state('3')
        f2.add_state('4')
        f2.add_state('5')
        f2.add_state('6')

        # now let's define our start and end state
        f2.initial_state = 'start'
        f2.set_final('6')

        ending = word[-1]

        for item in word:
            if item == 'w':
                f2.add_arc('start', '1', item, item)
            elif item == 's':
                f2.add_arc('start', '2', item, item)
            elif item == 'p':
                f2.add_arc('start', '3', item, item)
            elif item is 'h':
                f2.add_arc('start', '4', item, item)
            elif item is 'l':
                f2.add_arc('start', '5', item, item)
            f2.add_arc('1', '1', item, item)
            f2.add_arc('2', '2', item, item)
            f2.add_arc('3', '3', item, item)
            f2.add_arc('4', '4', item, item)
            f2.add_arc('5', '5', item, item)
            f2.add_arc('6', '6', item, ())

            if item == 'k' and ending == 'd':
                f2.add_arc('3', '6', item, '+past form')
                f2.add_arc('4', '6', item, '+past form')
                f2.add_arc('5', '6', item, item + "+past form")

            if (item == 'c' or item == 't') and ending == 'd':
                f2.add_arc('1', '6', item, item + "+past form")
                f2.add_arc('2', '6', item, item + "+past form")

            if item == 'k' and ending == 'g':
                f2.add_arc('3', '6', item, '+present participle form')
                f2.add_arc('4', '6', item, '+present participle form')
                f2.add_arc('5', '6', item, item + "+present participle form")

            if (item == 'c' or item == 't') and ending == 'g':
                f2.add_arc('1', '6', item, item + "+present participle form")
                f2.add_arc('2', '6', item, item + "+present participle form")

        output = f2.transduce(word)[0]
        return "".join(output)

if __name__ == '__main__':
    havoc = ['l', 'i', 'c', 'k', '+past form']
    myParser = Parser()
    print(myParser.generate(havoc))
    panic = list("synced")
    print(myParser.parse(panic))
