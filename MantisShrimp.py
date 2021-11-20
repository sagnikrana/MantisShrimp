from telethon import TelegramClient, events
import uuid
import asyncio

# Remember to use your own values from my.telegram.org!
api_id = 16673677
api_hash = '7380011e47f4b986ac80b40239a668b2'
user_target_channel = 'https://t.me/test_group_srana'
user_input_channel = 'https://t.me/Regular_H1B_H4_VisaSlotsChecking'
# user_input_channel = 'https://t.me/mockVisaSlot'

def generateUniqueSession():
    return uuid.uuid4().hex[:6].upper()


class Message:

    def __init__(self):
        self.stopWords = ['na', 'all', 'not', 'where', 'ofc', 'no']
        self.targetWord = 'avail'
        self.message = None
        self.totalMessagesAllTime = 0
        self.totalSuccessfulMessages = 0
        self.allTimeProbability = None
        self.statsMessage = None

    async def findGoodMessage(self):
        async with TelegramClient(generateUniqueSession(), api_id, api_hash) as client:

            @client.on(events.NewMessage(chats=user_input_channel))
            async def newMessageListener(event):
                self.message = event.message.message.lower()
                self.totalMessagesAllTime += 1
                if not self.isStopWordInMessage():
                    if self.targetWord in self.message:
                        self.totalSuccessfulMessages += 1
                        self.allTimeProbability = '{0:.2g}'.format(self.totalSuccessfulMessages / self.totalMessagesAllTime)
                        self.statsMessage = "Probability(useful messages) : "+self.allTimeProbability
                        await client.forward_messages(entity=user_target_channel, messages=event.message)
                        await client.send_message(user_target_channel, self.statsMessage)

            await client.run_until_disconnected()

    def isStopWordInMessage(self):
        for stopWord in self.stopWords:
            if stopWord in self.message:
                return True
        return False

    def asyncLoop(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.findGoodMessage())
        loop.close()


if __name__ == '__main__':
    message = Message()
    message.asyncLoop()