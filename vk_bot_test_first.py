import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

import re
import random


def main():
    vk_session = vk_api.VkApi(
        token="
    longpoll = VkBotLongPoll(vk_session, "219545110")
    is_registered = True
    start_reg = False
    is_playing = False
    qwestion_base = []
    for event in longpoll.listen():
        vk = vk_session.get_api()

        if not is_registered:
            if hasattr(event, 'source_act') and event.source_act == 'chat_invite_user':
                source_mid = event.source_mid
                keyboard = VkKeyboard(one_time=True)

                keyboard.add_button('Регистрация', color=VkKeyboardColor.PRIMARY)

                vk.messages.send(user_id=source_mid,
                                 message="Вам необходимо зарегистрироваться",
                                 keyboard=keyboard.get_keyboard(),
                                 random_id=random.randint(0, 2 ** 64))
            if start_reg:
                if event.type == VkBotEventType.MESSAGE_NEW:
                    number = event.obj.message['text']
                    print(number)
                    result = re.match(
                        r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$', number)
                    if bool(result):
                        keyboard = VkKeyboard(one_time=True)

                        keyboard.add_button('Правила', color=VkKeyboardColor.SECONDARY)
                        keyboard.add_button('Играть', color=VkKeyboardColor.POSITIVE)
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message="Вы успешно зарегистрировались",
                                         keyboard=keyboard.get_keyboard(),
                                         random_id=random.randint(0, 2 ** 64))
                        is_registered = True
                        start_reg = False
                    else:
                        keyboard = VkKeyboard(one_time=True)

                        keyboard.add_button('Регистрация', color=VkKeyboardColor.PRIMARY)
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message="Некорректный номер телефона",
                                         keyboard=keyboard.get_keyboard(),
                                         random_id=random.randint(0, 2 ** 64))
                        start_reg = False
            else:
                if event.type == VkBotEventType.MESSAGE_NEW:
                    if event.obj.message['text'] == 'Регистрация':
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message="Введите номер телефона",
                                         random_id=random.randint(0, 2 ** 64))
                        start_reg = True
                    else:

                        keyboard = VkKeyboard(one_time=True)

                        keyboard.add_button('Регистрация', color=VkKeyboardColor.PRIMARY)

                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message="Вам необходимо зарегистрироваться",
                                         keyboard=keyboard.get_keyboard(),
                                         random_id=random.randint(0, 2 ** 64))
        elif not is_playing:
            if event.type == VkBotEventType.MESSAGE_NEW:
                if event.obj.message['text'] == 'Правила':
                    keyboard = VkKeyboard(one_time=True)

                    keyboard.add_button('Правила', color=VkKeyboardColor.SECONDARY)
                    keyboard.add_button('Играть', color=VkKeyboardColor.POSITIVE)
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message="RULES_RULES_RULES",
                                     keyboard=keyboard.get_keyboard(),
                                     random_id=random.randint(0, 2 ** 64))
                elif event.obj.message['text'] == 'Играть':
                    # id - Text - Type - Media - Type_ans - Correct_ans - Name_film - Link
                    base = [(1, "Question", "picture", "1.jpg", "qw;er;ty", "FILMMM", "HTTP://"),
                            (2, "Question", "picture", "2.jpg", "qw;er;ty", "FILMMM", "HTTP://"),
                            (3, "Question", "picture", "3.jpg", "qw;er;ty", "FILMMM", "HTTP://")]
                    qwestion_base = random.choices(base, k=2)
                    random.shuffle(qwestion_base)
                    is_playing = True
                    tmp = qwestion_base[0]
                    keyboard = VkKeyboard(one_time=True)
                    answers = list(tmp[4].split(';'))
                    random.shuffle(answers)
                    keyboard.add_button(answers[0], color=VkKeyboardColor.SECONDARY)
                    keyboard.add_button(answers[1], color=VkKeyboardColor.SECONDARY)
                    keyboard.add_button(answers[2], color=VkKeyboardColor.SECONDARY)
                    if tmp[2] == 'picture':
                        upload = vk_api.VkUpload(vk)
                        photo = upload.photo_messages(tmp[3])
                        owner_id = photo[0]['owner_id']
                        photo_id = photo[0]['id']
                        access_key = photo[0]['access_key']
                        attachment = f'photo{owner_id}_{photo_id}_{access_key}'
                        print(2313213123)
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message=f"{tmp[1]}",
                                         attachment=attachment,
                                         keyboard=keyboard.get_keyboard(),
                                         random_id=random.randint(0, 2 ** 64))
                    else:
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message=f"{tmp[1]}",
                                         keyboard=keyboard.get_keyboard(),
                                         random_id=random.randint(0, 2 ** 64))
                else:
                    keyboard = VkKeyboard(one_time=True)

                    keyboard.add_button('Правила', color=VkKeyboardColor.SECONDARY)
                    keyboard.add_button('Играть', color=VkKeyboardColor.POSITIVE)
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message="Выберите:",
                                     keyboard=keyboard.get_keyboard(),
                                     random_id=random.randint(0, 2 ** 64))
        elif is_playing:
            pass

main()
