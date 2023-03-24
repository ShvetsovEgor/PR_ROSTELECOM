import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

import re
import random


def main():
    vk_session = vk_api.VkApi(
        token="print(123123)
    longpoll = VkBotLongPoll(vk_session, "219545110")
    is_registered = True
    start_reg = False
    is_playing = False
    # id - Text - Type - Media - Type_ans - Correct_ans - Name_film - Link
    base = {'1': ["Question", "picture", "1.jpg", "qw;er;ty", "er", "FILMMM", "HTTP://"],
            '2': ["Question", "picture", "2.jpg", "qw;er;ty", "er", "FILMMM", "HTTP://"],
            '3': ["Question", "picture", "3.jpg", "qw;er;ty", "er", "FILMMM", "HTTP://"]}
    current_question = None
    used_questions = []
    taken_questions = 0
    correct_ans = 0
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
        elif not current_question:
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
                    if len(used_questions) + 2 > len(list(base.keys())):
                        keyboard = VkKeyboard(one_time=True)

                        keyboard.add_button('Правила', color=VkKeyboardColor.SECONDARY)
                        keyboard.add_button('Играть', color=VkKeyboardColor.POSITIVE)
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message="Попытки закончились. Выберите дальнейшие действия:",
                                         keyboard=keyboard.get_keyboard(),
                                         random_id=random.randint(0, 2 ** 64))
                        continue
                    taken_questions += 1
                    current_question = random.choices(list(base.keys()))[0]
                    while current_question in used_questions:
                        current_question = random.choices(list(base.keys()))[0]
                    used_questions += [current_question]
                    print(current_question)
                    keyboard = VkKeyboard(one_time=True)
                    tmp = base[current_question]
                    answers = list(tmp[3].split(';'))
                    random.shuffle(answers)
                    keyboard.add_button(answers[0], color=VkKeyboardColor.SECONDARY)
                    keyboard.add_button(answers[1], color=VkKeyboardColor.SECONDARY)
                    keyboard.add_button(answers[2], color=VkKeyboardColor.SECONDARY)
                    if tmp[1] == 'picture':
                        upload = vk_api.VkUpload(vk)
                        photo = upload.photo_messages(tmp[2])
                        owner_id = photo[0]['owner_id']
                        photo_id = photo[0]['id']
                        access_key = photo[0]['access_key']
                        attachment = f'photo{owner_id}_{photo_id}_{access_key}'
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message=f"{tmp[0]}",
                                         attachment="video-219545110_456239017%2Fd1fa5134157be6dce9", #attachment,
                                         keyboard=keyboard.get_keyboard(),
                                         random_id=random.randint(0, 2 ** 64))
                    else:
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message=f"{tmp[0]}",
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
        elif current_question:
            if event.type == VkBotEventType.MESSAGE_NEW:
                tmp = base[current_question]
                if tmp[4] == event.obj.message['text']:
                    correct_ans += 1
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=f"Верно! {tmp[5]} {tmp[6]}",
                                     random_id=random.randint(0, 2 ** 64))
                else:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=f"Не верно! {tmp[5]} {tmp[6]}",
                                     random_id=random.randint(0, 2 ** 64))
                if taken_questions >= 2:
                    current_question = None
                    taken_questions = 0
                    keyboard = VkKeyboard(one_time=True)

                    keyboard.add_button('Правила', color=VkKeyboardColor.SECONDARY)
                    keyboard.add_button('Играть', color=VkKeyboardColor.POSITIVE)
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=f"Ваш результат: {correct_ans}",
                                     keyboard=keyboard.get_keyboard(),
                                     random_id=random.randint(0, 2 ** 64))
                    correct_ans = 0
                else:
                    taken_questions += 1
                    current_question = random.choices(list(base.keys()))[0]
                    while current_question in used_questions:
                        current_question = random.choices(list(base.keys()))[0]
                    used_questions += [current_question]
                    keyboard = VkKeyboard(one_time=True)
                    tmp = base[current_question]
                    answers = list(tmp[3].split(';'))
                    random.shuffle(answers)
                    keyboard.add_button(answers[0], color=VkKeyboardColor.SECONDARY)
                    keyboard.add_button(answers[1], color=VkKeyboardColor.SECONDARY)
                    keyboard.add_button(answers[2], color=VkKeyboardColor.SECONDARY)
                    if tmp[1] == 'picture':
                        upload = vk_api.VkUpload(vk)
                        photo = upload.photo_messages(tmp[2])
                        owner_id = photo[0]['owner_id']
                        photo_id = photo[0]['id']
                        access_key = photo[0]['access_key']
                        attachment = f'photo{owner_id}_{photo_id}_{access_key}'
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message=f"{tmp[0]}",
                                         attachment=attachment,
                                         keyboard=keyboard.get_keyboard(),
                                         random_id=random.randint(0, 2 ** 64))

main()
