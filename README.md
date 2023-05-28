4chan-picrel
================
This is a fork of the [4chan-downloader](https://github.com/Exceen/4chan-downloader) script. 
It retains most functionality from the original script, with considerable improvements. 
It records which files have been downloaded in each thread to a json file, therefore making continuosly montioring a thread optional.
It also solves a redundancy of the original script, that by default duplicated all threads. 
It aims to quickly solve other issues as well, including making the documentation clearer.

### Download Script ###

The main script is called **picrel.py** and can be called like this: `python picrel.py [thread/filename]`

```
usage: picrel.py [-h] [-c] [-d] [-l] [-n] [-r] [-t] [-m] thread

positional arguments:
  thread              url of the thread (or filename; one url per line)

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

A list of all downloaded files is progressivley recorded in a `downloaded_files.json` file, which is saved within the same folder. 

To re-download all files again, you can just delete the `json` file and re-run the script.

To re-download single files, just delete the respective lines inside the `json` file and re-run the script.

You can parse a queue file instead of a thread url. In this file you can put as many links as you want, you just have to make sure that there's one url per line. A line is considered to be a url if the first 4 letters of the line start with 'http'.

The queue file can also be generated via the Queue List Creator. See below.

### Requirements ###

This script can be called using the default python libraries. Only if you want to use the `--use-names` or `--title` parameters you have to install the following dependencies:
* Beautifulsoup4 >= 4.12.2 `pip install beautifulsoup4`
* Django >= 4.2.1 `pip install django`

### Queue List Creator ###

This script generates a queue list text file, which can be used by the main script to simultaneusly download media files from several threads. The user can specify several criteria to generate the list.

```
example usage: python queue-creator.py -b {board name} -q {text to search for in thread titles} -f {name of the file to save} -n {name of the directory}

arguments:
  -q, --query     the search terms(supports regex). This is required.
  -f, --queuefile     the name and extension of the queue file. This is required.
  -b, --board     the board name to search within
  -n, --naming      name of the directory where to save the threads
  -u, --thread-url  base urls of the chan boards  (default: https://boards.4chan.org/{board}/thread/{id}/{name})')
  -a, --api-url     base url of the chans api (default: https://a.4cdn.org/{board}/catalog.json)')
  -d, --directory     use or create the {board}/{name} directory, and place the queue file there

```

The script will looks for all threads titles that include `-q` inside the `-b` board, stores the thread url into `-f` and adds `-n` at the end of the url so that you can parse that value when using the `--use-names` argument from the actual download script.

### TODO ###

fix duplicated filenames when running with `--title`
