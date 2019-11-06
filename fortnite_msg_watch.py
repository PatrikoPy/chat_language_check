import fortnitepy
import csv
import lang_pattern


class MyClient(fortnitepy.Client):
    def __init__(self):
        super().__init__(
            email=input("fortnite account email: ").strip("\n"),
            password=input("password: ").strip("\n"),
            net_cl='8371783'
        )

    async def event_ready(self):
        print('----------------')
        print('Client ready as')
        print(self.user.display_name)
        print(self.user.id)
        print('----------------')

    # async def event_friend_request(self, request):
    #     await request.accept()
    #
    # async def event_party_invite(self, invitation):
    #     await invitation.accept()

    async def event_friend_message(self, message):
        print(f'Received message from {message.author.display_name} | Content: "{message.content}"')
        match = lang_pattern.check_message(message.content, lang_pattern.make_pattern("pattern_file.txt"), "en")
        if match:
            await message.reply("LANGUAGE ALERT")
            with open('FortniteLog.tsv', 'a', newline='') as tsv_file:
                tsv_writer = csv.writer(tsv_file, delimiter='\t')
                tsv_writer.writerow(
                    [str(message.created_at), message.author.display_name, message.content, 'friend message', match])

    async def event_party_message(self, message):
        print(f'Received message from {message.author.display_name} | Content: "{message.content}"')
        match = lang_pattern.check_message(message.content, lang_pattern.make_pattern("pattern_file.txt"), "en")
        if match:
            await message.reply("LANGUAGE ALERT")
            with open('FortniteLog.tsv', 'a', newline='') as tsv_file:
                tsv_writer = csv.writer(tsv_file, delimiter='\t')
                tsv_writer.writerow(
                    [str(message.created_at), message.author.display_name, message.content, 'party message', match])


def main():
    client = MyClient()
    client.run()


if __name__ == "__main__":
    main()
