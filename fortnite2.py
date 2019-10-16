import fortnitepy
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


class MyClient(fortnitepy.Client):
    def __init__(self):
        super().__init__(
            email='chatka_na_marsie@gmail.com',
            password='Sh1nigami',
            net_cl='8371783'
        )

    async def event_ready(self):
        print('----------------')
        print('Client ready as')
        print(self.user.display_name)
        print(self.user.id)
        print('----------------')

    async def event_friend_request(self, request):
        await request.accept()

    async def event_party_invite(self, invitation):
        await invitation.accept()

    async def event_friend_message(self, message):
        print(f'Received message from {message.author.display_name} | Content: "{message.content}"')
        lang_details = cld2.detect(message.content)
        if lang_details[2][0][1] == "en" or lang_details[2][0][1] == "un":
            print(lang_details[2][0][1])
            if re.search(pattern, message.content):
                await message.reply("you kiss your mother with that mouth?")
                with open('FortniteLog.tsv', 'a', newline='') as tsv_file:
                    tsv_writer = csv.writer(tsv_file, delimiter='\t')
                    tsv_writer.writerow(
                        [str(message.created_at), message.author.display_name, message.content, 'friend message'])

    async def event_party_message(self, message):
        print(f'Received message from {message.author.display_name} | Content: "{message.content}"')
        lang_details = cld2.detect(message.content)
        if lang_details[2][0][1] == "en" or lang_details[2][0][1] == "un":
            print(lang_details[2][0][1])
            if re.search(pattern, message.content):
                await message.reply("you kiss your mother with that mouth?")
                with open('FortniteLog.tsv', 'a', newline='') as tsv_file:
                    tsv_writer = csv.writer(tsv_file, delimiter='\t')
                    tsv_writer.writerow(
                        [str(message.created_at), message.author.display_name, message.content, 'party message'])


if __name__ == "__main__":
    pattern = make_pattern("s_words.txt")
    client = MyClient()
    client.run()
