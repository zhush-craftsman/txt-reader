import curses
import novelmanager
import locale


# ################### 常量定义 Start ###################
MAIN_WIN_WIDTH = 96
MAIN_WIN_HEIGHT = 20
MAIN_X = 0
MAIN_Y = 0
# ################### 常量定义 End ###################

# -- Give screen module scope
screen = None

# -- Define the appearance of some interface elements
hotkey_attr = curses.A_BOLD | curses.A_UNDERLINE
menu_attr = curses.A_NORMAL


# -- Create the topbar menu
def topbar_menu(menus):
    left = 2
    for menu in menus:
        menu_name = menu[0]
        menu_hotkey = menu_name[0]
        menu_no_hot = menu_name[1:]
        screen.addstr(1, left, menu_hotkey, hotkey_attr)
        screen.addstr(1, left+1, menu_no_hot, menu_attr)
        left = left + len(menu_name) + 3
    # Little aesthetic thing to display application title
    screen.addstr(1, left+30,
                  " TXT Reader",
                  curses.A_STANDOUT)
    screen.refresh()


def draw_book_list(win, selected, nlist):
    win.clear()
    win.box()
    for i in range(len(nlist)):
        book = '[' + str(i) + ']    ' + nlist[i]
        if i == selected:
            win.attron(curses.A_REVERSE)
            win.addstr(1+i, 2, book)
            win.attroff(curses.A_REVERSE)
        else:
            win.addstr(1+i, 2, book, curses.A_BOLD)
    win.refresh()


def book_list_view():
    global screen
    s = screen.subwin(MAIN_WIN_HEIGHT-1-1, MAIN_WIN_WIDTH-1-1, 2, 1)
    s.box()
    selected = 0
    nlist = list(map(lambda novel: novel['name'], novelmanager.getNovels()))
    draw_book_list(s, selected, nlist)
    s.keypad(1)
    while 1:
        k = s.getch()
        s.addstr(0, 0, str(k))
        if k in [curses.KEY_DOWN, ord('j')]:
            selected += 1
            if selected >= len(nlist):
                selected = 0
            draw_book_list(s, selected, nlist)
        elif k in [curses.KEY_UP, ord('k')]:
            selected -= 1
            if selected < 0:
                selected = len(nlist) - 1
            draw_book_list(s, selected, nlist)
        elif k == 10:
            return nlist[selected]


def draw_book_content(win, lines):
    win.clear()
    for i in range(len(lines)):
        win.move(i+1, 0)
        win.addnstr(lines[i], curses.COLS)
    # win.addstr(''.join(lines), curses.COLS)
    win.refresh()


def book_content_view(book):
    viewBeginX, viewBeginY = MAIN_X + 1, MAIN_Y + 2
    viewWidth, viewHeight = MAIN_WIN_WIDTH-1-1, MAIN_WIN_HEIGHT-1-1
    global screen
    s = screen.subwin(viewHeight, viewWidth, viewBeginY, viewBeginX)
    s.box()
    s.refresh()
    s.keypad(1)

    contentBeginX, contentBeginY = viewBeginX + 1, viewBeginY + 1
    contentWidth, contentHeight = viewWidth-1-1, viewHeight-1-1
    contentWin = s.subwin(contentHeight, contentWidth, contentBeginY, contentBeginX)

    contentRow = contentHeight - 2
    contentColumn = contentWidth - 2

    bookIter = novelmanager.read_book(1, contentRow, contentColumn//2)
    forward = None
    while True:
        try:
            lines = bookIter.send(forward)
            draw_book_content(contentWin, lines)
            k = s.getch()
            if k == 261:
                forward = 1
            elif k == 260:
                forward = -1
            elif k == ord('q'):
                break
        except StopIteration:
            break


# -- Magic key handler both loads and processes keys strokes
def topbar_key_handler(key_assign=None, key_dict={}):
    if key_assign:
        key_dict[ord(key_assign[0])] = key_assign[1]
    else:
        c = screen.getch()
        if c in (curses.KEY_END, ord('!')):
            return 0
        elif c not in key_dict.keys():
            curses.beep()
            return 1
        else:
            return eval(key_dict[c])


def draw_main(stdscr):
    locale.setlocale(locale.LC_ALL, "")
    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    global screen
    screen = stdscr.subwin(MAIN_WIN_HEIGHT, MAIN_WIN_WIDTH, MAIN_Y, MAIN_X)
    screen.box()
    screen.hline(2, 1, curses.ACS_HLINE, MAIN_WIN_WIDTH-1-1)
    screen.refresh()

    # Define the topbar menus
    file_menu = ("File", "file_func()")
    exit_menu = ("Exit", "EXIT")

    # Add the topbar menus to screen object
    topbar_menu((
        file_menu, exit_menu
    ))

    while True:
        bookToRead = book_list_view()

        book_content_view(bookToRead)

    # while topbar_key_handler():
    #     pass


def main():
    curses.wrapper(draw_main)


if __name__ == "__main__":
    main()
