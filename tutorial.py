import curses
from curses import wrapper # this will initialize the module and then return the terminal back to the previous state

# curses will involve some atypical syntax
def main(stdscr): # the input gives you a "superimposed screen"
    # first, we need to clear the entire screen
    stdscr.clear()
    stdscr.addstr("Hello World!")
    # refresh the screen
    stdscr.refresh()
    stcscr.getkey() # in practice, this adds a delay that will stop the screen from automatically closing.

wrapper(main) # strangely, 'wrapper' is a function that we pass main() to.
                # it'll call this function while initializing everything to this module.



