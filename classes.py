import requests
import time
import settings

class User:
    def __init__(self, test_user_id, test_user_token):
        self.user_id = test_user_id
        self.token = test_user_token
        self.groups = []
        self.friends = []
        self.service_token = settings.service_token
        self.params = settings.params

    def get_response(self, api_method, params):
        response = requests.get(settings.api_vk_url+api_method, params)
        try:
            if response.json()['error']['error_code'] == 6:
                time.sleep(2)
                response = requests.get(settings.api_vk_url + api_method, params)
        # finally:
        #     return response.json()
        # 2) get_response есть try но нет exept так задуманно?
        #
        # Да, это сделал специально, try нужен только для того, чтобы получить повторный response,
        # в случае, если превышен лимит запросов к api vk.
        # Если использовать except, можно написать так:
        except KeyError:
            return response.json()
        return response.json()

    def get_groups(self):
        settings.params['extended'] = 1
        settings.params['fields'] = 'gid,name,members_count'
        response = self.get_response(settings.get_groups_method, settings.params)
        count = response['response']['count'] - 1
        while count >= 0:
            self.groups.append(
                {
                    'name': response['response']['items'][count]['name'],
                    'gid': response['response']['items'][count]['id'],
                    'members_count': response['response']['items'][count]['members_count']
                }
            )
            count -= 1

    def get_friends(self):
        response = self.get_response(settings.get_friends_method, settings.params)
        self.friends = response['response']['items']

    def is_members(self, users, group):
        settings.params['access_token'] = settings.service_token
        settings.params['group_id'] = group
        settings.params['user_ids'] = users
        response = self.get_response(settings.is_members_method, settings.params)
        return response['response']

    def check_user_id(self):
        settings.params['user_id'] = ''
        settings.params['user_ids'] = settings.user_id
        response = self.get_response(settings.check_user_id_method, settings.params)
        try:
            if response['error']['error_code'] == 113:
                print('Неверно указан идентификатор пользователя.')
                exit()
            elif response['error']['error_code'] == 5:
                print('Неверно указан токен пользователя.')
                exit()
        except KeyError:
            settings.params['user_id'] = int(response['response'][0]['id'])