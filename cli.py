import requests
import json
import time
import curses

# Initialize curses
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)

# Initialize variables
completed_delivery_stops = 0
previous_completed_delivery_stops = 0
previous_time = time.time()
stop_num = 71

while True:
    # Make API call
    url = 'https://apis.track.dpdlocal.co.uk/v1/routes/0000*00000*000*0000'
    response = requests.get(url)

    # Parse JSON response
    data = json.loads(response.text)

    # Update the number of completed delivery stops
    completed_delivery_stops = data['data']['completedDeliveryStops']

    # Check if the number of completed delivery stops has changed
    if completed_delivery_stops != previous_completed_delivery_stops:
        current_time = time.time()
        # get the time elapsed since last change
        time_elapsed = current_time - previous_time
        minutes, seconds = divmod(time_elapsed, 60)
        formatted_time_elapsed = f"{int(minutes)} minutes {int(seconds)} seconds"
        
        # Estimate time until the next stop
        if completed_delivery_stops < stop_num:
            remaining_stops = stop_num - completed_delivery_stops
            avg_time_per_stop = time_elapsed / (completed_delivery_stops - previous_completed_delivery_stops)
            estimated_time = avg_time_per_stop * remaining_stops
            hours, minutes = divmod(estimated_time/60, 60)
            seconds = estimated_time % 60
            formatted_est_time = f"{int(hours)} hours {int(minutes)} minutes {int(seconds)} seconds"
        
        # Clear the screen
        stdscr.clear()

        # Update the information on the terminal
        stdscr.addstr(0, 0, f'Number of completed delivery stops: {completed_delivery_stops}')
        stdscr.addstr(1, 0, f'Time elapsed since last change: {formatted_time_elapsed}')
        stdscr.addstr(2, 0, f'Estimated time until stop {stop_num}: {formatted_est_time}')

        # Refresh the screen
        stdscr.refresh()

        previous_completed_delivery_stops = completed_delivery_stops
        previous_time = current_time
    time.sleep(10)

# Deinitialize curses
curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()
