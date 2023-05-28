import bot_utils.bot_config

from bot_utils.bot_config import ACCESS_TOKEN, GROUP_ID
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

vk_session = VkApi(token=ACCESS_TOKEN)
long_poll = VkBotLongPoll(vk_session, GROUP_ID)


def sender(message: str = "", chat_id: str = bot_utils.bot_config.CHAT_ID, ) -> None:
    vk_session.method('messages.send', {
        'chat_id': chat_id,
        'message': message,
        'random_id': 0,
    })


def main():
    for event in long_poll.listen():
        print(event.type)

        if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat:
            chat_id = event.chat_id
            print("chat id is {}".format(chat_id))
            input_message = event.object.message['text'].lower()
            if input_message == "да это репчик":
                sender("лол я кринжУю с тебЯ", chat_id)
            else:
                sender("шо?")


if __name__ == "__main__":
    main()
