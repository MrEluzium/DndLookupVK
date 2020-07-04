import vk_api
import lookup_5e
from Settings import TOKEN
from vk_api.utils import get_random_id
from vk_api.longpoll import VkLongPoll, VkEventType
token = TOKEN
vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)


def write_msg(user_id, message=None, attachment=None):
    vk.messages.send(
        user_id=user_id,
        random_id=get_random_id(),
        message=message,
        attachment=attachment
    )


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            request = event.text
            # if request == "привет":
            #    write_msg(event.user_id, "Хай", "photo-99100481_457239042")
            answer1 = str(lookup_5e.main(request))
            user_info = vk.users.get(user_ids=event.user_id)[0]
            if answer1 == "Not Found":
                print(f"{user_info['first_name']} {user_info['last_name']}({user_info['id']}) | {request} | Fail")
            else:
                print(f"{user_info['first_name']} {user_info['last_name']}({user_info['id']}) | {request} | Success")
            to_sent = True
            while to_sent:
                answer2 = answer1[:4096]
                answer1 = answer1[4096:]
                write_msg(event.user_id, answer2)
                to_sent = False if len(answer2) < 4096 else True