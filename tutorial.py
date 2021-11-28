import curses
from curses import wrapper # this will initialize the module and then return the terminal back to the previous state

# curses will involve some atypical syntax
def main(stdscr): # the input gives you a "superimposed screen"
    # using I.D. 1, it's green foreground and a white background.
    # we could have multiple pairs of colors; using I.D 1 for the first pair makes sense
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    # first, we need to clear the entire screen
    stdscr.clear()
    stdscr.addstr(1,0,"Hello World!") # color_pair() is built-in. Go one line down and start at zeroth character.
    # refresh the screen
    stdscr.refresh()
    stdscr.getkey() # in practice, this adds a delay that will stop the screen from automatically closing.

wrapper(main) # strangely, 'wrapper' is a function that we pass main() to.
                # it'll call this function while initializing everything to this module.




