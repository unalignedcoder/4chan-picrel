#!/usr/bin/python3
import urllib.request, urllib.error, urllib.parse, argparse, logging
import os, re, time
import http.client 
import fileinput
from multiprocessing import Process
import json

log = logging.getLogger('picrel')
workpath = os.path.dirname(os.path.realpath(__file__))

args = None

def main():
    global args
    parser = argparse.ArgumentParser(description='picrel')
    parser.add_argument('thread', nargs=1, help='url of the thread (or filename; one url per line)')
    parser.add_argument('-c', '--with-counter', action='store_true', help='show a counter next the the image that has been downloaded')
    parser.add_argument('-d', '--date', action='store_true', help='show date as well')
    parser.add_argument('-l', '--less', action='store_true', help='show less information (suppresses checking messages)')
    parser.add_argument('-n', '--use-names', action='store_true', help='use thread names instead of the thread ids (...4chan.org/board/thread/thread-id/thread-name)')
    parser.add_argument('-r', '--reload', action='store_true', help='reload the queue file every 5 minutes')
    parser.add_argument('-t', '--title', action='store_true', help='save original filenames')
    parser.add_argument('-m', '--monitor', action='store_true', help='keep monitoring a fast thread')
    args = parser.parse_args()

    if args.date:
        logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s', datefmt='%Y-%m-%d %I:%M:%S %p')
    else:
        logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s', datefmt='%I:%M:%S %p')    

    if args.title:
        try:
            import bs4
            import django
        except ImportError:
            logging.error('Could not import the required modules! Disabling --title option...')
            args.title = False

    thread = args.thread[0].strip()

    if thread[:4].lower() == 'http':
        download_thread(thread, args)
    else:
        download_from_file(thread)

def load(url):
    req = urllib.request.Request(url, headers={'User-Agent': '4chan Browser'})
    return urllib.request.urlopen(req).read()

def get_title_list(html_content):
    ret = list()

    from bs4 import BeautifulSoup
    parsed = BeautifulSoup(html_content, 'html.parser')
    divs = parsed.find_all("div", {"class": "fileText"})

    for i in divs:
        current_child = i.findChildren("a", recursive = False)[0]
        try:
            ret.append(current_child["title"])
        except KeyError:
            ret.append(current_child.text)

    return ret

def call_download_thread(thread_link, args, downloaded_files):
    try:
        download_thread(thread_link, args, downloaded_files)
    except KeyboardInterrupt:
        pass

def download_thread(thread_link, args, downloaded_files):
    board = thread_link.split('/')[3]
    thread = thread_link.split('/')[5].split('#')[0]
    if len(thread_link.split('/')) > 6:
        thread_tmp = thread_link.split('/')[6].split('#')[0]

        if args.use_names or os.path.exists(os.path.join(workpath, 'downloads', board, thread_tmp)):                
            thread = thread_tmp

    thread_folder = os.path.join(workpath, 'downloads', board, thread)
    downloaded_files = load_downloaded_files(thread_folder)  # Load the downloaded files from the JSON file
    new_files_downloaded = False  # Flag to track if new files were downloaded

    while True:
        try:
            regex = '(\/\/i(?:s|)\d*\.(?:4cdn|4chan)\.org\/\w+\/(\d+\.(?:jpg|png|gif|webm)))'
            html_result = load(thread_link).decode('utf-8')
            regex_result = list(set(re.findall(regex, html_result)))
            regex_result = sorted(regex_result, key=lambda tup: tup[1])
            regex_result_len = len(regex_result)
            regex_result_cnt = 1

            directory = os.path.join(workpath, 'downloads', board, thread)
            if not os.path.exists(directory):
                os.makedirs(directory)

            if args.title:
                all_titles = get_title_list(html_result)

            for enum_index, enum_tuple in enumerate(regex_result):
                link, img = enum_tuple

                if args.title:
                    img = all_titles[enum_index]
                    from django.utils.text import get_valid_filename
                    img_path = os.path.join(directory, get_valid_filename(img))
                else:
                    img_path = os.path.join(directory, img)

                if img_path not in downloaded_files:
                    data = load('https:' + link)

                    output_text = board + '/' + thread + '/' + img
                    if args.with_counter:
                        output_text = '[' + str(regex_result_cnt).rjust(len(str(regex_result_len))) +  '/' + str(regex_result_len) + '] ' + output_text

                    log.info(output_text)

                    with open(img_path, 'wb') as f:
                        f.write(data)

                    # Add the downloaded file to the recorded list
                    downloaded_files.append(img_path)
                    new_files_downloaded = True  # Set the flag to indicate new files were downloaded
                    save_downloaded_files(downloaded_files, thread_folder)  # Save the updated list to the JSON file

                regex_result_cnt += 1    

        except urllib.error.HTTPError:
            time.sleep(10)
            try:
                load(thread_link)    
            except urllib.error.HTTPError:
                log.info('%s 404\'d', thread_link)
                break
            continue
        except (urllib.error.URLError, http.client.BadStatusLine, http.client.IncompleteRead):
            log.fatal(thread_link + ' crashed!')
            raise

        if not new_files_downloaded:
            log.info('No new media files to download. Operation stopped.')
            save_downloaded_files(downloaded_files, thread_folder)  # Save the downloaded files to the JSON file
            break

        if not args.less:
            log.info('Checking ' + board + '/' + thread)

        if args.monitor:
            time.sleep(20)
        else:
            log.info('No new media files to download. Operation stopped.')
            break

def download_from_file(filename):
    running_links = []
    while True:
        processes = []
        #queue_file = os.path.join(os.path.abspath(workpath), filename)
        queue_file = workpath + filename
        #log.info('your queue path:' + queue_file)
        for link in [_f for _f in [line.strip() for line in open(queue_file) if line[:4] == 'http'] if _f]:
            if link not in running_links:
                running_links.append(link)
                log.info('Added ' + link)

            board = link.split('/')[3]
            thread = link.split('/')[5].split('#')[0]
            thread_folder = os.path.join(workpath, 'downloads', board, thread)

            downloaded_files = load_downloaded_files(thread_folder)
            process = Process(target=call_download_thread, args=(link, args, downloaded_files))
            process.start()
            processes.append([process, link])

        if len(processes) == 0:
            log.warning(filename + ' empty')
        
        if args.reload:
            time.sleep(60 * 5) # 5 minutes
            links_to_remove = []
            for process, link in processes:
                if not process.is_alive():
                    links_to_remove.append(link)
                else:
                    process.terminate()

            for link in links_to_remove:
                for line in fileinput.input(filename, inplace=True):
                    print(line.replace(link, '-' + link), end='')
                running_links.remove(link)
                log.info('Removed ' + link)
            if not args.less:
                log.info('Reloading ' + args.thread[0]) # thread = filename here; reloading on the next loop
        else:
            break

def load_downloaded_files(thread_folder):
    downloaded_files = []
    json_file = os.path.join(thread_folder, 'downloaded_files.json')

    if os.path.exists(json_file):
        with open(json_file, 'r') as f:
            downloaded_files = json.load(f)

    return downloaded_files

def save_downloaded_files(downloaded_files, thread_folder):
    json_file = os.path.join(thread_folder, 'downloaded_files.json')

    with open(json_file, 'w') as f:
        json.dump(downloaded_files, f)
        f.flush()
        os.fsync(f)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
