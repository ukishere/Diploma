import requests
import time
import settings

class User:
    def __init__(self):
        self.groups = []
        self.friends = []
        self.service_token = settings.service_token
        self.params = settings.params

    def get_response(self, api_method, params):
        self.response = requests.get(settings.api_vk_url+api_method, params)
        try:
            if self.response.json()['error']['error_code'] == 6:
                time.sleep(2)
                self.response = requests.get(settings.api_vk_url + api_method, params)
        finally:
            return self.response.json()

    def get_groups(self):
        self.count = 0
        settings.params['extended'] = 1
        settings.params['fields'] = 'gid,name,members_count'
        self.response = self.get_response('groups.get', settings.params)
        self.count = self.response['response']['count'] - 1
        while self.count >= 0:
            self.groups.append(
                {
                    'name': self.response['response']['items'][self.count]['name'],
                    'gid': self.response['response']['items'][self.count]['id'],
                    'members_count': self.response['response']['items'][self.count]['members_count']
                }
            )
            self.count -= 1

    def get_friends(self):
        self.response = self.get_response('friends.get', settings.params)
        self.friends = self.response['response']['items']

    def is_members(self, users, group):
        settings.params['access_token'] = settings.service_token
        settings.params['group_id'] = group
        settings.params['user_ids'] = users
        self.response = self.get_response('groups.isMember', settings.params)
        return self.response['response']

    def check_user_id(self):
        settings.params['user_id'] = ''
        settings.params['user_ids'] = settings.user_id
        self.response = self.get_response('users.get', settings.params)
        try:
            if self.response['error']['error_code'] == 113:
                print('Неверно указан идентификатор пользователя.')
                exit()
            elif self.response['error']['error_code'] == 5:
                print('Неверно указан токен пользователя.')
                exit()
        except KeyError:
            settings.params['user_id'] = int(self.response['response'][0]['id'])