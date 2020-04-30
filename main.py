import json
import requests
import time

class User:
    def __init__(self):
        self.token = ''
        self.user_ID = ''
        self.groups = []
        self.friends = []
        self.service_token = 'c6e5ee88c6e5ee88c6e5ee8842c6946c62cc6e5c6e5ee88984cd96bcef7d96ba884c9e1'

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
        try:
            if self.response.json()['error']['error_code'] == 6:
                time.sleep(2)
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
        except KeyError:
            pass
        finally:
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
        try:
            if self.response.json()['error']['error_code'] == 6:
                time.sleep(2)
                self.response = requests.get(
                    'https://api.vk.com/method/friends.get',
                    params={
                        'access_token': self.token,
                        'user_id': self.user_ID,
                        'v': 5.103,
                    }
                )
                self.friends = self.response.json()['response']['items']
        except KeyError:
            self.friends = self.response.json()['response']['items']

    def isMembers(self, users, group):
        self.response = requests.get(
        'https://api.vk.com/method/groups.isMember',
        params={
            'access_token': self.service_token,
            'group_id': group,
            'user_ids': users,
            'v': 5.103,
        }
        )
        try:
            if self.response.json()['error']['error_code'] == 6:
                time.sleep(1)
                self.response = requests.get(
                    'https://api.vk.com/method/groups.isMember',
                    params={
                        'access_token': self.service_token,
                        'group_id': group,
                        'user_ids': users,
                        'v': 5.103,
                    }
                )
                return self.response.json()['response']
        except KeyError:
            return self.response.json()['response']

    def checkUserID(self):
        self.response = requests.get(
        'https://api.vk.com/method/users.get',
        params={
            'access_token': self.token,
            'user_ids': self.user_ID,
            'v': 5.103,
        }
        )
        try:
            if self.response.json()['error']['error_code'] == 113:
                print('Неверно указан идентификатор пользователя.')
                exit()
            elif self.response.json()['error']['error_code'] == 5:
                print('Неверно указан токен пользователя.')
                exit()
            elif self.response.json()['error']['error_code'] == 6:
                time.sleep(2)
                self.user_ID = int(self.response.json()['response'][0]['id'])
        except KeyError:
            self.user_ID = int(self.response.json()['response'][0]['id'])

def find_friends_in_group(test_user, friends):
    found = 0
    member_friends = test_user.isMembers(friends, group['gid'])
    for member_friend in member_friends:
        if member_friend['member'] == 1:
            found += 1
    return found

def groups_output(groups):
    count = 1
    for group in groups:
        print(f"{count}. {group['name']}")
        count += 1

test_user = User()
#test_user.user_ID = '171691064'
test_user.user_ID = 'eshmargunov'
test_user.token = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
max_friends_in_group = 0

print('Входные данные.')
print(f'Имя или ID пользователя: {test_user.user_ID}')
print(f'Токен пользователя: {test_user.token}')
print(f'Максимальное количество друзей в группе: {max_friends_in_group}')

print('Начало работы.')
test_user.checkUserID()
print('Входные данные проверены.')
test_user.getGroups()
print('Список групп пользователя получен.')
test_user.getFriends()
print('Список друзей пользователя получен.')

unique_groups = []
groups_count = 0
friends_count = 0
percent = 0

for group in test_user.groups:
    groups_total = len(test_user.groups)
    found = 0
    friends = ''

    print(f"[{'*' * (percent // 10)}{' ' * (10 - percent // 10)}] Проанализировано {percent}% групп.")

    for friend in test_user.friends:
        friends = friends + str(friend) + ','
        friends_count += 1
        if friends_count == 500:
            found += find_friends_in_group(test_user, friends)
            friends = ''
            friends_count = 0
    found += find_friends_in_group(test_user, friends)

    if found <= max_friends_in_group:
        unique_groups.append(group)

    groups_count += 1
    percent = round(groups_count/groups_total*100)

print(f"[{'*' * 10}] Проанализировано 100% групп.")

if len(unique_groups) == 0:
    print('Групп, удовлетворяющих условиям не найдено.\nСоздан пустой файл.')
    file = open('groups.json', 'w')
    file.close()
else:
    print('Следующие группы удовлетворяют условиям:')
    groups_output(unique_groups)
    with open('groups.json', 'w', encoding='utf-8') as file:
        json.dump(unique_groups, file, indent=2, ensure_ascii=False)
    print('Данные записаны в файл.')