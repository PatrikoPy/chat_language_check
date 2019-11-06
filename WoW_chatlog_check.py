import csv
import lang_pattern
import os


def open_file():
    while True:
        try:
            # current directory
            new_file = open("WoWChatlog.txt", encoding="UTF-8")
            break
        except FileNotFoundError:
            try:
                # default directory
                new_file = open(os.path.join("C:/Program Files/World of Warcraft/", "WoWChatlog.txt"), encoding="UTF-8")
            except FileNotFoundError:
                try:
                    # user input directory
                    new_file = open(os.path.join(input("Copy a path to WoWChatlog.txt file:\n"), "WoWChatlog.txt"),
                                    encoding="UTF-8")
                    break
                except FileNotFoundError:
                    print("Error: wrong path")
                    continue
    return new_file


def wow_msg_parser(line):
    msg_parsed = ['', '', '', '']  # [date&time, author, content, channel]
    msg_parsed[0] = line[0:18].rstrip(' ')
    line = line[18:].lstrip(' ')
    if line.startswith('['):
        msg_parsed[3] = line[1:line.index(']')]
        line = line[line.index(']') + 1:].lstrip(' ')
        msg_parsed[1] = line[:line.index(':')]
        msg_parsed[2] = (line[line.index(':'):].lstrip(': ')).rstrip('\n')
    elif 'says:' in line:
        msg_parsed[3] = 'Say'
        msg_parsed[1] = line.split('says:', 1)[0].strip()
        msg_parsed[2] = line.split('says:', 1)[1].strip(' \n')
    elif 'yells:' in line:
        msg_parsed[3] = 'Yell'
        msg_parsed[1] = line.split('yells:', 1)[0].strip()
        msg_parsed[2] = line.split('yells:', 1)[1].strip(' \n')
    else:
        return None
    return msg_parsed


def main():
    # setup of a new empty file
    with open('WoWLog.tsv', 'w', newline='', encoding='utf-8-sig') as tsv_file:
        tsv_writer = csv.writer(tsv_file, delimiter='\t')
    pattern = lang_pattern.make_pattern("pattern_file.txt")
    chatlog_file = open_file()
    for line in chatlog_file:
        my_message = wow_msg_parser(line)
        if my_message:
            match = lang_pattern.check_message(my_message[2], pattern, "en")
            if match:
                with open('WoWLog.tsv', 'a', newline='', encoding='utf-8-sig') as tsv_file:
                    tsv_writer = csv.writer(tsv_file, delimiter='\t')
                    tsv_writer.writerow(
                        [my_message[0], my_message[1], my_message[2], my_message[3].rstrip('\n'), match])
    chatlog_file.close()


if __name__ == '__main__':
    main()
