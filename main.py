import requests


def move(snake, target, others, fences):
    enemy_coordinates = []
    for enemy in others:
        enemy_coordinates.extend(enemy['geometry'])
    head = snake['geometry'][0]
    for i, (head_coordinate, target_coordinate) in enumerate(zip(head, target)):
        difference = target_coordinate - head_coordinate
        if difference:
            distance = difference // abs(difference)
            new_head = head.copy()
            new_head[i] += distance
            if new_head in fences + enemy_coordinates:
                continue
            snake['direction'] = [0, 0, 0]
            snake['direction'][i] = distance
            break


def get_distance(coordinates1, coordinates2):
    total = 0
    for coordinate1, coordinate2 in zip(coordinates1, coordinates2):
        total += abs(coordinate1 - coordinate2)
    return total


def get_target(snake, food, others):
    head = snake['geometry'][0]
    shortest = float('+inf')
    target = None
    for mandarin in food:
        distance = get_distance(head, mandarin['c'])
        if mandarin['points'] <= 0:
            continue
        for enemy in others:
            if enemy['geometry']:
                enemy_head = enemy['geometry'][0]
                if get_distance(enemy_head, mandarin['c']) < distance:
                    break
        else:
            if shortest > distance:
                shortest = distance
                target = mandarin['c']
    return target


def main():
    # Ваш токен

    token = '2340525d-595b-4de5-8f44-3946ca3baa43'

    # URL сервера

    server_url = 'https://games-test.datsteam.dev/play/snake3d'

    # API-метод

    api = '/player/move'

    url = f"{server_url}{api}"

    # Заголовки запроса

    headers = {

        'X-Auth-Token': token,

        'Content-Type': 'application/json',

        'Accept-Encoding': 'gzip'

    }

    # Данные для отправки

    data = {

        'snakes': []

    }

    while True:
        try:
            response = requests.post(url, headers=headers, json=data)
            response = response.json()
        except Exception as ex:
            print(response)

        snakes = response['snakes']

        for snake in snakes:
            if snake['status'] == 'dead':
                continue
            teammates = [other for other in snakes if snake is not other]
            others = response['enemies'] + teammates
            print(snake['geometry'][0], snake['direction'])
            target = get_target(snake, response['food'], others)
            if target:
                move(snake, target, others, response['fences'])

        data = {
            'snakes': snakes
        }


if __name__ == '__main__':
    main()
