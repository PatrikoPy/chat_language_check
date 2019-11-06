import re
import cld2


def make_pattern(filename):
    words = []
    with open(filename, "r") as file:
        for line in file:
            words.append(line.strip('\n'))
    new_pattern = r"\b(" + "|".join(words).strip("|") + r")\b"
    return re.compile(new_pattern, re.IGNORECASE)


def check_message(message_content, pattern, set_lang="en"):
    lang_details = cld2.detect(message_content)
    lang = (lang_details[2][0][1])
    if lang == set_lang or lang == "un":
        if re.search(pattern, message_content):
            return lang
        else:
            return None
