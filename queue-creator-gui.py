import PySimpleGUI as sg
import subprocess
import threading
import sys

def run_queue_creator(board, query, queuefile, naming, thread_url=None, api_url=None, directory=False):
    # Define the command to execute the queue-creator script
    cmd = ['python', 'queue-creator.py', '-b', board, '-q', query, '-f', queuefile, '-n', naming]
    
    if thread_url:
        cmd.extend(['-u', thread_url])
    
    if api_url:
        cmd.extend(['-a', api_url])
    
    if directory:
        cmd.append('-d')
    
    # Execute the queue-creator script
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    while True:
        line = process.stdout.readline()
        if not line:
            break
        print(line.strip())
    
    process.wait()
    
    if process.returncode == 0:
        print('Queue file created:', queuefile)
    else:
        print('Error:', process.stderr.read())

def create_queue_gui(board, query, queuefile, naming, thread_url=None, api_url=None, directory=False):
    # Create a separate thread for running the queue-creator script
    thread = threading.Thread(target=run_queue_creator, args=(board, query, queuefile, naming, thread_url, api_url, directory))
    thread.start()

# Set the theme and font for the window
sg.theme('GreenMono')
sg.set_options(font=('Arial', 14))

# Define the layout
layout = [
    [sg.Text('Board name:'), sg.Input(key='-BOARD-')],
    [sg.Text('Search terms:'), sg.Input(key='-QUERY-')],
    [sg.Text('Name of the Queue File:'), sg.Input(key='-QUEUEFILE-'), sg.FileSaveAs()],
    [sg.Text('Search name:'), sg.Input(key='-NAMING-')],
    #[sg.Text('Thread URL (optional):'), sg.Input(key='-THREADURL-')],
    #[sg.Text('API URL (optional):'), sg.Input(key='-APIURL-')],
    [sg.Checkbox('Save queue file in Board Directory', key='-DIRECTORY-')],
    [sg.Button('Create Queue File'), sg.Button('Exit')],
    [sg.Output(size=(60, 10), key='-OUTPUT-')]
]

# Create the window
window = sg.Window('4chan-picrel / Queue File Creator', layout)

# Event loop
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Exit':
        break
    elif event == 'Create Queue':
        board = values['-BOARD-']
        query = values['-QUERY-']
        queuefile = values['-QUEUEFILE-']
        naming = values['-NAMING-']
        #thread_url = values['-THREADURL-']
        #api_url = values['-APIURL-']
        directory = values['-DIRECTORY-']
        
        if not queuefile:
            print('Please specify a queue file.')
        elif not board:
            print('Please specify a board.')
        elif not query:
            print('Please specify a query.')
        elif not naming:
            print('Please specify a naming convention.')
        else:
            #print('Creating queue file...')
            #create_queue_gui(board, query, queuefile, naming, thread_url, api_url, directory)
            create_queue_gui(board, query, queuefile, naming, directory)

# Close the window
window.close()
