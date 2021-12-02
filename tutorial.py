import curses
from curses import wrapper # this will initialize the module and then return the terminal back to the previous state

def start_screen(stdscr): # we need access to stdscr to write things to the screen
    stdscr.clear()
    stdscr.addstr("Welcome to the typing speed test!") # color_pair() is built-in.
    stdscr.addstr("\nPress any key to begin.") # remember new line syntax
    # refresh the screen
    stdscr.refresh()
    stdscr.getkey() # in practice, this adds a delay that will stop the screen from automatically closing.


# to get the typed text to display over the target text
def display_text(stdscr, target, current, wpm=0): # =0 makes it an optional parameter
    stdscr.addstr(target) # color_pair() is built-in.

    for i, char in enumerate(current): # this will give us the element and the current text
        stdscr.addstr(0, i, char, curses.color_pair(1)) # we'll display those characters on the screen in a different color.
                    # whatever the index is (starting at 0), it will get overlaid on top of target_text as 'i' is incremented by +1.

    # The original way of doing this:
    # for char in current_text: # next, we loop through every character that they've typed
    #   stdscr.addstr(char, curses.color_pair(1)) # we'll display those characters on the screen in a different color.


def wpm_test(stdscr):
    target_text = "Hello world this is a text."
    current_text = []
  
    while True:
        # how to show the target_text first ...
        stdscr.clear() # if you don't clear the screen, it will add back everything you've typed so far
        display_text(stdscr, target_text, current_text)
        stdscr.refresh() # then, we refresh the screen
        
        # ... then ask the user to hit a key.
        key = stdscr.getkey() # this waits for the user to type something
        
        if ord(key) == 27: # the ASCII representation of your keyboard for 'esc'
            break

        if key in ('KEY_BACKSPACE', '\b', '\x7f'):  # if the key is a backspace (on almsot any keyboard) ...
            # we'll need to pop off the last element from the list so that our backspaces don't mess things up. 
            if len(current_text) > 0:
                current_text.pop()
        else:
            current_text.append(key) # when they type, it gets appedned to the current text

# curses will involve some atypical syntax
def main(stdscr): # the input gives you a "superimposed screen"
    # using I.D. 1, it's green foreground and a white background.
    # we could have multiple pairs of colors; using I.D 1 for the first pair makes sense
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    start_screen(stdscr)
    wpm_test(stdscr)

wrapper(main) # strangely, 'wrapper' is a function that we pass main() to.
                # it'll call this function while initializing everything to this module.




