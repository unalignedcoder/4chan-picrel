import PySimpleGUI as sg
import subprocess
import threading

def run_picrel_script(url, use_names, reload_queue, use_titles, monitor_thread):
    # Define the command to execute the picrel script
    cmd = ['python', 'picrel.py', url]

    if use_names:
        cmd.append('-n')
    if reload_queue:
        cmd.append('-r')
    if use_titles:
        cmd.append('-t')
    if monitor_thread:
        cmd.append('-m')

    # Execute the picrel script
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

    while True:
        line = process.stdout.readline()
        if not line:
            break
        print(line.strip())

    process.wait()

def run_script():
    # Disable the 'Run' button while the script is running
    window['-RUN-'].update(disabled=True)

    # Clear the output before running the script
    window['-OUTPUT-'].update('')

    # Get the selected values from the GUI
    url = values['-THREAD_URL-']
    use_names = values['-USE_NAMES-']
    reload_queue = values['-RELOAD-']
    use_titles = values['-TITLE-']
    monitor_thread = values['-MONITOR-']

    # Create a separate thread for running the picrel script
    thread = threading.Thread(target=run_picrel_script, args=(url, use_names, reload_queue, use_titles, monitor_thread))
    thread.start()

def exit_script():
    # Close the window
    window.close()

# Set the color theme for the GUI
sg.theme('GreenMono')
sg.set_options(font=('Arial', 14))

# Create the GUI layout
layout = [
    [sg.Text('Thread URL or Queue file'), sg.Input(key='-THREAD_URL-')],
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
        exit_script()
        break
    elif event == '-RUN-':
        run_script()

