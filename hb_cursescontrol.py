import curses

class control(object):
    def __init__(self):
        # get the curses screen window
        self.screen = curses.initscr()
        # turn off input echoing
        curses.noecho()
        # respond to keys immediately (don't wait for enter)
        curses.cbreak()
        # map arrow keys to special values
        self.screen.keypad(True)
        #self.screen.border(0)

    def get_key(self):
        char = self.screen.getch()
        if char == ord('q'):
            #break
            return "q"
        elif char == curses.KEY_RIGHT:
            # print doesn't work with curses, use addstr instead
            #screen.addstr(0, 0, 'right')
            return "right"
        elif char == curses.KEY_LEFT:
            #screen.addstr(0, 0, 'left ')
            return "left"
        elif char == curses.KEY_UP:
            #screen.addstr(0, 0, 'up   ')
            return "up"
        elif char == curses.KEY_DOWN:
            #screen.addstr(0, 0, 'down ')
            return "down"
        elif char == curses.KEY_ENTER:
            #screen.addstr(0, 0, 'enter ')
            return "enter"
        else:
            return char

    def quit_nicely(self):
        curses.endwin()

    def read_key_loop(self):
        char = 0
        #self.screen.addstr(12, 25, "Waiting for key...")
        #self.screen.refresh()
        while char != ('q'):
            char = self.get_key()
            #self.screen.clear()
            #self.screen.border(0)
            #self.screen.addstr(12, 25, "Waiting for key...")
            #self.screen.addstr(13, 25, "You pushed = " + str(char))
            #self.screen.refresh()
            print char


if __name__ == "__main__":
    import time
    import hb_cursescontrol

    test = hb_cursescontrol.control()
    test.read_key_loop()
    test.quit_nicely()
