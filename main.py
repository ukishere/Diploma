import json
import classes
import settings

def find_friends_in_group(test_user, friends, group):
    found = 0
    member_friends = test_user.is_members(friends, group['gid'])
    for member_friend in member_friends:
        if member_friend['member'] == 1:
            found += 1
    return found

def groups_output(groups):
    count = 1
    for group in groups:
        print(f"{count}. {group['name']}")
        count += 1

def starter():
    test_user = classes.User()
    test_user.user_id = settings.user_id
    test_user.token = settings.user_token

    print('Входные данные.')
    print(f'Имя или ID пользователя: {test_user.user_id}')
    print(f'Токен пользователя: {test_user.token}')
    print(f'Максимальное количество друзей в группе: {settings.max_friends_in_group}')

    print('Начало работы.')
    test_user.check_user_id()
    print('Входные данные проверены.')
    test_user.get_friends()
    print('Список друзей пользователя получен.')
    test_user.get_groups()
    print('Список групп пользователя получен.')

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
                found += find_friends_in_group(test_user, friends, group)
                friends = ''
                friends_count = 0
        found += find_friends_in_group(test_user, friends, group)

        if found <= settings.max_friends_in_group:
            unique_groups.append(group)

        groups_count += 1
        percent = round(groups_count / groups_total * 100)

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

if __name__ == '__main__':
    starter()



