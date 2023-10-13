4chan-picrel
================
This is a fork of the [4chan-downloader](https://github.com/Exceen/4chan-downloader) script. 
It retains most functionality from the original script, with considerable improvements:
- It adds a GUI interface for ease of use;
- It records which files have been downloaded in each thread to a json file, therefore making continuosly montioring a thread optional;
- It solves a redundancy of the original script, that by default duplicated all threads;
- It makes the documentation clearer.

## Install ##
- Have Python
- Install [requirements](#requirements).

## GUI Interface ##

Double-click on `picrel-gui.py` and you are good to go. 

![image](https://github.com/unalignedcoder/4chan-picrel/assets/16850566/c3d6c6d1-e37b-475b-bdc9-26fdb63807d0)

This is based on [PySimpleGUI](https://github.com/PySimpleGUI/PySimpleGUI). 
It interacts with the main download script allowing the user to avoid commandline instructions.
The script can be also used directly, of course, as preferred.

## Main Download Script ##

The main script is called **picrel.py**.

```
usage: python picrel.py [-h] [-c] [-d] [-l] [-n] [-r] [-t] [-m] thread/queue

positional arguments:
  thread/queue              url of the thread (or queue text file which contains one url per line)

optional arguments:
  -h, --help          show this help message and exit
  -c, --with-counter  show a counter next the the image that has been
                      downloaded
  -d, --date          show date as well
  -l, --less          show less information (surpresses checking messages)
  -n, --use-names     use thread names instead of the thread ids
                      (...4chan.org/board/thread/thread-id/thread-name)
  -r, --reload        reload the queue file every 5 minutes
  -t, --title         save original filenames
  -m, --monitor       keep monitoring a fast thread
```
The script creates a `/downloads/<board name>/<thread id or thread name>/` folder where all media files are saved.

A list of all downloaded files is progressivley recorded in `downloaded_files.json`, which is saved within the same folder. 

To re-download all files again, you can just delete the `json` file and re-run the script.

To re-download single files, just delete the respective lines inside the `json` file and re-run the script.

You can parse a queue file instead of a thread url. In this file you can put as many links as you want, you just have to make sure that there's one url per line. A line is considered to be a url if the first 4 letters of the line start with 'http'.

The queue file can also be generated via the [Queue List Creator](https://github.com/unalignedcoder/4chan-picrel/blob/master/README.md#queue-list-creator). See below.

## Requirements ##

In order to use the GUI, you need to install `PySimpleGUI`.

The `Beautifulsoup4` and `Django` libraries are also required.

Best way to go about this is to open terminal from the script directory and run:
`pip install -r requirements.txt`

## Queue List Creator ##

Double click on `queue-creator-gui.py` and you are good to go.

![image](https://github.com/unalignedcoder/4chan-picrel/assets/16850566/7537e9ca-90fb-4ac6-8a3e-28e7b66997bf)

This script searches 4chan for your query and generates a queue list text file, which can be used by the main script to simultaneusly download media files from several threads. The user can specify several criteria to generate the list.

```
usage: python queue-creator.py [-q] {search term} [-f] {file name} [-b] {board name} [-n] {name of the search} 
    [-u] [-a] [-d] {specify whether to save the queue file under a board/directory path}

arguments:
  -q, --query         the search terms(supports regex). This is required.
  -f, --queuefile     the name and extension of the queue file. This is required.
  -b, --board         the board name to search within
  -n, --naming        name of the search (can be later used to name the directory where to save the threads)
  -u, --thread-url    base urls of the chan boards  (default: https://boards.4chan.org/{board}/thread/{id}/{name})
  -a, --api-url       base url of the chans api (default: https://a.4cdn.org/{board}/catalog.json)
  -d, --directory     use or create the {board}/{name} directory, and place the queue file there

```

The script will look for all threads titles that include `--query` inside the `--board` board, store the thread url into `--queuefile` and add `--naming` at the end of the url so that you can parse that value later, when using the `--use-names` argument from the actual download script.The `--directory` argument is useful to separate different thread lists.
