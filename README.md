4chan-picrel
================
This is a fork of the [4chan-downloader](https://github.com/Exceen/4chan-downloader) script. 
It has all functionality of the original script, but it remembers which files were downloaded in each thread, therefore making continuosly montioring a thread optional.

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
  -m, --monitor       keep monitoring a fast thread (off by default, as the list of downloaded files is saved in a json file and files are not downloaded twice)
```

You can parse a file instead of a thread url. In this file you can put as many links as you want, you just have to make sure that there's one url per line. A line is considered to be a url if the first 4 letters of the line start with 'http'.

If you use the --use-names argument, the thread name is used to name the respective thread directory instead of the thread id.

### Requirements ###

This script can be called using the default python libraries. Only if you want to use the `--use-names` or `--title` parameters you have to install the following requirements:
* Beautifulsoup4 >= 4.12.2 `pip install beautifulsoup4`
* Django >= 4.2.1 `pip install django`

### Thread Watcher ###

This is a work-in-progress script but basic functionality is already given. If you call the script like

`python thread-watcher.py -b vg -q mhg -f queue.txt -n "Monster Hunter"`

then it looks for all threads that include `mhg` inside the `vg` board, stores the thread url into `queue.txt` and adds `/Monster-Hunter` at the end of the url so that you can use the --use-names argument from the actual download script.

### Legacy ###

The current scripts are written in python3, in case you still use python2 you can use an old version of the script inside the legacy directory.

### TODO ###

fix duplicated filenames when running with `--title`
