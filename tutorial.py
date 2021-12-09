import curses
from curses import wrapper # this will initialize the module and then return the terminal back to the previous state
import time
import random

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
    stdscr.addstr(1, 0, f"WPM: {wpm}")  # we'll place the f-string one line below the target text

    for i, char in enumerate(current): # this will give us the element and the current text
        correct_char = target[i]  # telling us what the correct character would be
        color = curses.color_pair(1)
        if char != correct_char:
            color = curses.color_pair(2)

        stdscr.addstr(0, i, char, color) # we'll display those characters on the screen in green or red.
                    # whatever the index starts at (in this case, 0), it will get overlaid on top of target_text as the 'i' is incremented by +1.

    # The original way of doing this:
    # for char in current_text: # next, we loop through every character that they've typed
    #   stdscr.addstr(char, curses.color_pair(1)) # we'll display those characters on the screen in a different color.

def load_text(): # thsi will select from random lines inteh text file
    with open("text.txt", "r") as f: #'with' (which is a context manager) closes the file after we have read it.
        lines = f.readlines()            # this will give us a list containing all the lines in this file 'f'.
        return random.choice(lines).strip()# we want to randomly choose a line from 'f'. .strip() removes the invisible \n (or other leading/trailing) characters at the end of each line.

def wpm_test(stdscr):
    target_text = load_text()
    current_text = []
    wpm = 0 # initalize it to 0
    start_time = time.time() # will tell us what the time is when we started the loop.
    stdscr.nodelay(True)

    while True:
        time_elapsed = max(time.time() - start_time, 1) # '1' helps us not divide by 0 below (which is impossible)
        wpm = round((len(current_text) / (time_elapsed/60)) / 5)  # this gives us words per minute (assuming the average word is 5 characters long)
                                                                    # lastly, we round it to avoid unmanageable decimals
                                                                    # wpm will be calculated every time we hit a key
        # how to show the target_text first ...
        stdscr.clear() # if you don't clear the screen, it will add back everything you've typed so far
        display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh() # then, we refresh the screen
        
        if "".join(current_text) == target_text:  # turns the list into a string
            # giving it an empty string ("") join to stacks the characters all into one continuous string
            stdscr.nodelay(False) # making nodelay into False gives the user a chance to hit a key
            break  # the user succeeded, so we can break out of the game while loop

        # ... then ask the user to hit a key. But we still this to be counting down on time, even if we're not typing.
        try:
            key = stdscr.getkey() # this waits for the user to type something
                                # 'try' makes sure that it won't crash on us if the user stops typing ...
        except: # ... if there is a crash, then we tell it to 'continue' by going back to the top of the while loop.
            continue  # this is necessary because there's no 'key' to carry on with.

        if ord(key) == 27: # the ASCII representation of your keyboard for 'esc'
            break

        if key in ('KEY_BACKSPACE', '\b', '\x7f'):  # if the key is a backspace (on almsot any keyboard) ...
            # we'll need to pop off the last element from the list so that our backspaces don't mess things up. 
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target_text): # prevents us from exceeding the characters of the target text.
            current_text.append(key) # when they type, it gets appended to the current text

# curses will involve some atypical syntax
def main(stdscr): # the input gives you a "superimposed screen"
    # using I.D. 1, it's green foreground and a white background.
    # we could have multiple pairs of colors; using I.D 1 for the first pair makes sense
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    start_screen(stdscr)
    
    while True:
        wpm_test(stdscr)
        stdscr.addstr(2,0, "You completed the test! Press any key to continue ...")
        key = stdscr.getkey()  
        if ord(key) == 27:  # if the key is anything other than 'Esc', then the game continues
            break

wrapper(main) # strangely, 'wrapper' is a function that we pass main() to.
                # it'll call this function while initializing everything to this module.




