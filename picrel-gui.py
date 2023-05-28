import PySimpleGUI as sg
import subprocess
import threading
import queue

class OutputRedirector:
    def __init__(self, queue):
        self.queue = queue

    def write(self, message):
        self.queue.put(message)

def get_selected_arguments():
    # Function to retrieve the selected arguments from the GUI
    # Modify this function to match your argument selection method
    arguments = []

    # Example: Retrieving values from input elements
    thread_url = values['-THREAD_URL-']
    arguments.append(thread_url)

    # Example: Retrieving values from checkboxes
    # if values['-WITH_COUNTER-']:
    #     arguments.append('-c')
    # if values['-DATE-']:
    #     arguments.append('-d')
    # if values['-LESS-']:
    #     arguments.append('-l')
    if values['-USE_NAMES-']:
        arguments.append('-n')
    if values['-RELOAD-']:
        arguments.append('-r')
    if values['-TITLE-']:
        arguments.append('-t')
    if values['-MONITOR-']:
        arguments.append('-m')

    return arguments

def run_script_thread(queue):
    # Get the selected arguments from the GUI
    args = get_selected_arguments()

    # Construct the command to run
    command = ["python", "picrel.py"]
    command.extend(args)

    # Run the command and capture the output
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

    # Read the output line by line and put it in the queue
    for output_line in process.stdout:
        queue.put(output_line)

    # Wait for the process to finish
    process.wait()

    # Put a sentinel value in the queue to indicate the end of the output
    queue.put(None)

def update_output(output_queue):
    while True:
        output_line = output_queue.get()
        if output_line is None:
            break
        window['-OUTPUT-'].print(output_line, end='')

def run_script():
    # Disable the 'Run' button while the script is running
    window['-RUN-'].update(disabled=True)

    # Clear the output before running the script
    window['-OUTPUT-'].update('')

    # Create a queue to capture the output
    output_queue = queue.Queue()

    # Start the script thread and the output update thread
    script_thread = threading.Thread(target=run_script_thread, args=(output_queue,))
    output_thread = threading.Thread(target=update_output, args=(output_queue,))

    script_thread.start()
    output_thread.start()

    # Wait for the script thread to finish
    script_thread.join()

    # Enable the 'Run' button after the script has finished
    window['-RUN-'].update(disabled=False)

# Set the color theme for the GUI
sg.theme('GreenMono')
sg.set_options(font=('Arial', 14))

# Create the GUI layout
layout = [
    [sg.Text('Thread URL or Queue file'), sg.Input(key='-THREAD_URL-')],
    #[sg.Checkbox('With Counter', key='-WITH_COUNTER-')],
    #[sg.Checkbox('Date', key='-DATE-')],
    #[sg.Checkbox('Less', key='-LESS-')],
    [sg.Checkbox('Use Thread Names', key='-USE_NAMES-')],
    [sg.Checkbox('Reload queue file', key='-RELOAD-')],
    [sg.Checkbox('Use Media Titles', key='-TITLE-')],
    [sg.Checkbox('Keep monitoring the thread', key='-MONITOR-')],
    [sg.Button('Run', key='-RUN-', size=(10, 1)), sg.Button('Exit', key='-EXIT-', size=(10, 1))],
    [sg.Output(size=(80, 10), key='-OUTPUT-')]
]

# Create the window
window = sg.Window('4chan-picrel / Media downloader', layout)

# Event loop
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == '-EXIT-':
        break
    elif event == '-RUN-':
        run_script()

# Close the window
window.close()
