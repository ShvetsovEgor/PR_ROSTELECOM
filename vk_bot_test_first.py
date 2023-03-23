import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

import re
import random


def main():
    vk_session = vk_api.VkApi(
        token="
    longpoll = VkBotLongPoll(vk_session, "219545110")
    is_registered = False
    start_reg = False
    for event in longpoll.listen():
        vk = vk_session.get_api()

        if not is_registered:
            if start_reg:
                if event.type == VkBotEventType.MESSAGE_NEW:
                    number = event.obj.message['text']
                    print(number)
                    result = re.match(
                        r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$', number)
                    if bool(result):
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message="Вы успешно зарегистрировались",
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
        else:
            keyboard = VkKeyboard(one_time=True)

            keyboard.add_button('Белая кнопка', color=VkKeyboardColor.SECONDARY)
            keyboard.add_button('Зелёная кнопка', color=VkKeyboardColor.POSITIVE)

            keyboard.add_line()  # Переход на вторую строку
            keyboard.add_location_button()

            keyboard.add_line()
            keyboard.add_vkpay_button(hash="action=transfer-to-group&group_id=74030368&aid=6222115")


main()
