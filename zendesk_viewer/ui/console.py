import curses
from curses import textpad

from pick import pick
from utils import string_utils

def draw_home_ui(client, user_name):
    client.reset()

    options = ['List tickets', 'Exit']
    title = 'Welcome to Zendesk ticket viewer, {}!'.format(user_name)
    subtitle = '=>'
    option, _ = pick(options, title, subtitle)

    if option == 'List tickets':
        tickets = client.get_tickets()
        draw_list_tickets_ui(client, user_name, tickets)
    elif option == 'Exit':
        exit()

def draw_list_tickets_ui(client, user_name, tickets):
    options = ['Go Home']
    title = 'My tickets'
    subtitle = '=>'

    for ticket in tickets:
        options.append(str(ticket['id']) + "\t" + ticket['status'].upper() + "\t" + ticket['subject'])
    
    if client.has_prev():
        options.append('Previous page')

    if client.has_next():
        options.append('Next page')
    
    option, index = pick(options, title, subtitle)

    if option == 'Go Home':
        draw_home_ui(client, user_name)
    elif option == 'Previous page':
        tickets = client.get_tickets('prev')
        draw_list_tickets_ui(client, user_name, tickets)
    elif option == 'Next page':
        tickets = client.get_tickets()
        draw_list_tickets_ui(client, user_name, tickets)
    else:
        curses.wrapper(draw_ticket_ui, client, user_name, tickets, tickets[index - 1])

def draw_ticket_ui(stdscr, client, user_name, tickets, ticket):
    k = 0

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # Loop where k is the last character pressed
    while (k != ord('b') and k != ord('q')):

        # Initialization
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        # Declaration of strings
        title = "TICKET DETAILS"
        statusbarstr = "Press 'b' or 'q' to go back"

        # Draw border
        writebox_uly = (int(stdscr.getbegyx()[0]))
        writebox_ulx = (int(stdscr.getbegyx()[1]))
        writebox_lry = (int(stdscr.getmaxyx()[0] * 0.96))
        writebox_lrx = (int(stdscr.getmaxyx()[1] - 1))

        textpad.rectangle(stdscr, writebox_uly, writebox_ulx, writebox_lry, writebox_lrx)

        # Centering calculations
        start_x_title = int((width // 2) - (len(title) // 2) - len(title) % 2)
        start_x = 2
        start_y = 1

        # Rendering some text
        stdscr.addstr(0, start_x_title, title, curses.color_pair(1))

        # Render status bar
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height-1, 0, statusbarstr)
        stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
        stdscr.attroff(curses.color_pair(3))

        # Turning on attributes for headings
        stdscr.attron(curses.color_pair(2))
        stdscr.attron(curses.A_BOLD)

        # Rendering headings
        stdscr.addstr(start_y + 1, start_x, "SUBJECT")
        stdscr.addstr(start_y + 3, start_x, "STATUS")
        stdscr.addstr(start_y + 5, start_x, "CREATED AT")
        stdscr.addstr(start_y + 7, start_x, "UPDATED AT")
        stdscr.addstr(start_y + 9, start_x, "TAGS")
        stdscr.addstr(start_y + 11, start_x, "DESCRIPTION")

        # Turning off attributes for headings
        stdscr.attroff(curses.color_pair(2))
        stdscr.attroff(curses.A_BOLD)

        # Render values
        stdscr.addstr(start_y + 1, start_x + 15, ticket['subject'])
        stdscr.addstr(start_y + 3, start_x + 15, ticket['status'].upper())
        stdscr.addstr(start_y + 5, start_x + 15, ticket['created_at'])
        stdscr.addstr(start_y + 7, start_x + 15, ticket['updated_at'])
        stdscr.addstr(start_y + 9, start_x + 15, "; ".join(ticket['tags']))

        # Render description
        _y = 11
        line_len = width - start_x - 18
        for line in ticket['description'].split('\n\n'):
            chunks = string_utils.chunkstring(line, line_len)
            for chunk in chunks:
                stdscr.addstr(start_y + _y, start_x + 15, chunk)
                _y += 1
            _y += 1

        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        k = stdscr.getch()
    
    draw_list_tickets_ui(client, user_name, tickets)

def draw_error_ui(stdscr, title, *subtitles):
    k = 0

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    while (k != ord('q')):    
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        
        # Centering calculations
        start_x_title = int((width // 2) - (len(title) // 2) - len(title) % 2)
        start_y = int((height // 2) - 2)
        
        # Render status bar
        statusbarstr = "Press 'q' to exit"
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height-1, 0, statusbarstr)
        stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
        stdscr.attroff(curses.color_pair(3))

        # Turning on attributes for title
        stdscr.attron(curses.color_pair(2))
        stdscr.attron(curses.A_BOLD)

        # Rendering title
        stdscr.addstr(start_y, start_x_title, title)

        # Turning off attributes for title
        stdscr.attroff(curses.color_pair(2))
        stdscr.attroff(curses.A_BOLD)

        # Print subtitles
        for subtitle in subtitles:
            start_x_subtitle = int((width // 2) - (len(subtitle) // 2) - len(subtitle) % 2)
            stdscr.addstr(start_y + 1, start_x_subtitle, subtitle)
            start_y += 1
        
        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        k = stdscr.getch()

def show_error(title, *subtitles):
    curses.wrapper(draw_error_ui, title, *subtitles)