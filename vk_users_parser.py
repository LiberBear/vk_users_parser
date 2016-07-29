import vk_api
import configparser
def captcha_handler(captcha):
    key = input("Enter Captcha {0}: ".format(captcha.get_url())).strip()
    return captcha.try_again(key)

def parse_ids(group_id, tools):
    ids = tools.get_all('groups.getMembers', 1000, {'group_id': group_id})
    ids = ids['items']
    return ids
def read_groups():
    group_list = []
    f=open('groups.txt', 'r')
    for line in f:
        group_list.append(line.strip())
    f.close
    return group_list
def write_ids(data):
    with open('result.txt', 'w') as f:
        for line in data:
            f.write(str(line) + '\n')
def main():
    parsed = []
    filtered = []
    #Берем список груп из файла
    group_list = read_groups()
    # Загружаем конфиг
    conf = configparser.RawConfigParser()
    conf.read('config.cfg')
    login = conf.get('account', 'login')
    password = conf.get('account', 'password')
    print('Loggin into ' + login)
    vk_session = vk_api.VkApi(login, password, captcha_handler=captcha_handler)
    try:
        vk_session.authorization()
    except vk_api.AuthorizationError as error_msg:
        print(error_msg)
        return
    tools = vk_api.VkTools(vk_session)
    #Поочередно собираем все ид с каждой группы
    for group in group_list:
        print('Parsing ' + group)
        parsed = parsed + parse_ids(group, tools)
    #Удаляем дубликаты
    for user in parsed:
        if user not in filtered:
            filtered.append(user)
    #Результат пишем в result.txt и идем пить кофе
    write_ids(filtered)
    print('Done!')
    input('Press Enter...')
if __name__ == '__main__':
        main()
