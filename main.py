import json
from urllib.parse import urlencode
import requests

class User:
    def __init__(self):
        self.token = ''
        self.user_ID = ''
        self.groups = []
        self.friends = []

    def getGroups(self):
        self.groups = []
        self.count = 0
        self.response = requests.get(
            'https://api.vk.com/method/groups.get',
            params={
                'access_token': self.token,
                'user_id': self.user_ID,
                'extended': 1,
                'fields': 'gid,name,members_count',
                'v': 5.103,
            }
        )
        self.count = self.response.json()['response']['count'] - 1
        while self.count >= 0:
            self.groups.append(
                {
                    'name': self.response.json()['response']['items'][self.count]['name'],
                    'gid': self.response.json()['response']['items'][self.count]['id'],
                    'members_count': self.response.json()['response']['items'][self.count]['members_count']
                }
            )
            self.count -= 1

    def getFriends(self):
        self.response = requests.get(
            'https://api.vk.com/method/friends.get',
            params={
                'access_token': self.token,
                'user_id': self.user_ID,
                'v': 5.103,
            }
        )
        self.friends = self.response.json()['response']['items']

    def isMember(self, user, group):
        self.response = requests.get(
        'https://api.vk.com/method/groups.isMember',
        params={
            'access_token': service_token,
            'group_id': group,
            'user_id': user,
            'v': 5.103,
        }
        )
        return self.response.json()['response']

def groups_output(groups):
    count = 1
    for group in groups:
        print(f"{count}. {group['name']}")
        count += 1

########################################################

app_ID = 7439082
service_token = 'c6e5ee88c6e5ee88c6e5ee8842c6946c62cc6e5c6e5ee88984cd96bcef7d96ba884c9e1'
continuation = 'да'

while continuation == 'да' or continuation == 'lf':
    test_user = User()
    while True:
        authorisation = input('Выберете операцию:\n1. Авторизоваться.\n2. Использовать тестовый токен.\n')

        if authorisation == '1':
            parameters = {
                'client_id': app_ID,
                'display': 'page',
                'scope': 262146,
                'response_type': 'token',
                'v': '5.52'
            }

            test_user.user_ID = input('Введите логин или ID пользователя: ')
            print('Пройдите по следующей ссылке для получения токена:')
            print('?'.join(('https://oauth.vk.com/authorize', urlencode(parameters))))
            test_user.token = input('Введите полученный токен: ')

            break

        elif authorisation == '2':
            test_user.token = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
            test_user.user_ID = '171691064'

            break

        else:
            print('Неверный ввод.')

    test_user.getGroups()
    test_user.getFriends()

    unique_groups = []
    groups_total = len(test_user.groups)
    groups_count = 0
    friends_count = 0
    percent = 0

    for group in test_user.groups:
        found = False
        for friend in test_user.friends:
            if friends_count >= 10:
                friends_count = 0
            friends_count += 1

            print(f"[{'*'*friends_count}{' '*(10-friends_count)}] Проанализировано {percent}% групп.")
            if test_user.isMember(friend, group['gid']) == 1:
                found = True
        if not found:
            unique_groups.append(group)
        groups_count += 1
        percent = round(groups_count/groups_total*100)
    print('Анализ успешно завершен.')

    with open('groups.json', 'w', encoding='utf-8') as file:
        json.dump(unique_groups, file, indent=2, ensure_ascii=False)

    print(f'Файл сформирован.\nУникальные для пользователя c id{test_user.user_ID} группы:')
    groups_output(unique_groups)

    while True:
        continuation = input('Продолжить (да/нет)? ')
        continuation = continuation.lower().strip()
        if continuation == 'да' or continuation == 'нет' or continuation == 'lf' or continuation == 'ytn':
            break
        else:
            print('Неверный ввод.')