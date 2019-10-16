import csv
import re
import cld2


def make_pattern(filename):
    words = []
    with open(filename, "r") as file:
        for line in file:
            words.append(line.strip('\n'))
    s_pattern = r"\b(" + "|".join(words).strip("|") + r")\b"
    return re.compile(s_pattern, re.IGNORECASE)


pattern = make_pattern("s_words.txt")

# with open('WoWLog.tsv', 'w', newline='', encoding='utf-8-sig') as tsv_file:
#     tsv_writer = csv.writer(tsv_file, delimiter='\t')
with open('WoWChatlog.txt', 'r', encoding='utf-8-sig') as file:
    iterator = (i for i in range(10000))
    for line in file:
        tsv_list = ['', '', '', '', '']
        tsv_list[0] = line[0:18].rstrip(' ')
        line = line[18:].lstrip(' ')
        if line.startswith('['):
            tsv_list[3] = line[1:line.index(']')]
            line = line[line.index(']') + 1:].lstrip(' ')
            tsv_list[1] = line[:line.index(':')]
            tsv_list[2] = (line[line.index(':'):].lstrip(': ')).rstrip('\n')
        elif 'says:' in line:
            tsv_list[3] = 'Say'
            tsv_list[1] = line.split('says:', 1)[0].strip()
            tsv_list[2] = line.split('says:', 1)[1].strip(' \n')
        elif 'yells:' in line:
            tsv_list[3] = 'Yell'
            tsv_list[1] = line.split('yells:', 1)[0].strip()
            tsv_list[2] = line.split('yells:', 1)[1].strip(' \n')
        else:
            continue
        lang_details = cld2.detect(tsv_list[2])
        message = tsv_list[2]
        tsv_list[4] = (lang_details[2][0][1])
        # tsv_list[4] = (lang_details) #pełne info o języku
        if lang_details[2][0][1] == "en" or lang_details[2][0][1] == "un":
            # print(lang_details[2][0][1])
            if re.search(pattern, message):
                with open('WoWLog2.tsv', 'a', newline='', encoding='utf-8-sig') as tsv_file:
                    tsv_writer = csv.writer(tsv_file, delimiter='\t')
                    tsv_writer.writerow([tsv_list[0], tsv_list[1], tsv_list[2], tsv_list[3].rstrip('\n'), tsv_list[4]])

        if next(iterator) == 10000:
            break
