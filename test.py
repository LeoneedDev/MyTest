import redis
import psycopg2
import json
import random
from flask import Response

def API1():
    '''Функция первого задания'''
    print('Первый API')
    print('Введите хоста')
    host = input()
    print('Введите порт')
    port = int(input())

    r = redis.Redis(host=host, port=port)

    def chek_annagram(an1, an2):
        '''Проверяет на анаграмму слово, и возвращает True или False'''
        angrm1 = list(an1)
        angrm2 = list(an2)
        angrm1.sort()
        angrm2.sort()
        x = 0
        matches = True
        while x < len(an1) and matches:
            if angrm1[x] == angrm2[x]:
                x += 1
            else:
                matches = False
        return matches

    def json_answer(arg):
        '''Везвращает json ответ с числом из Redis и говорит анаграмма ли это'''
        getted = int(r.get('schet'))
        matches = arg + ' анаграммма'
        result = json.dumps([matches,getted])
        print(result)
        return result

    def last_function():
        '''Исполняющая функция'''
        print('Введите 1 слово')
        an1 = input()
        print('Введите 2 слово')
        an2 = input()
        matches = chek_annagram(an1, an2)
        if matches == True:
            '''Увеличивет число Redis и говорит что это анаграмма'''
            r.incr('schet')
            arg = 'ДА, это'
        elif matches == False:
            arg = 'Не'
        return json_answer(arg)

    return last_function()
API1()

def API2():
    '''Функция второго задания'''

    def random_name(names):
        '''Слуйчайное имя устройства'''
        result = random.choice(names)
        return result


    def connect_db(dbname,user,hostname,password,port):
        '''Подключается к базе данных'''
        connect = psycopg2.connect(dbname=dbname, user=user, host=hostname, password=password, port=port)
        try:
            cursor = connect.cursor()
            return connect,cursor
        except (Exception, psycopg2.Error) as error:
            print('Произошла ошибка с подключением, номер ошибки',error)


    def close_connect(connect,cursor):
        '''Закрывает соеденение с postgresql'''
        cursor.close()
        connect.close()


    def random_hex():
        '''Создает случайную последовательность 48 бит и преобразует в hex формат'''
        bits = random.getrandbits(48)
        result = hex(bits)
        return result

    def API3(cursor):
        '''Возвращает длину списка груперованного по dev_type'''
        cursor.execute("SELECT dev_type FROM devices LEFT JOIN endpoints on endpoints.device_id=devices.id WHERE endpoints.comment IS NULL GROUP BY devices.dev_type;")
        table = cursor.fetchall()
        len_table = len(table)
        return len_table

    def insert_db():
        '''Функция внедряет в БД необходимые данные'''
        print('Второй API')
        print('Введите dbname')
        dbname = input()
        print('Введите user')
        user = input()
        print('Введите hostname')
        hostname = input()
        print('Введите password')
        password = input()
        print('Введите port')
        port = input()
        connect, cursor = connect_db(dbname, user, hostname, password, port)
        try:
            l = []
            names = ['emeter', 'zigbee', 'lora', 'gsm']

            '''Я возможно не так понял задание с endpoints'''
            enpoints = ('endpoint1', 'endpoit2', 'endpoint3')

            '''Добовляет 10 устройств со случайным значениями dev_type and dev_id'''
            for x in range(10):
                cursor.execute('INSERT INTO devices(dev_type,dev_id) VALUES(%s,%s) RETURNING id;', (random_name(names), random_hex()))
                id_of_new_row = cursor.fetchone()[0]
                l.append(id_of_new_row)
            random.shuffle(l)
            connect.commit()
            for x in l[0:5]:
                try:
                    '''Для случайных 5 девайсов добовляем в endpoints значение endpoint'''
                    cursor.execute("INSERT INTO endpoints (device_id,comment) VALUES (%s,%s);", (x,(random.choice(enpoints))))
                    connect.commit()
                    '''Возможно что вернуть тут тоже не понял, вроде как HTTP response но я так и непонял
                        как имеено это дожно работать'''
                    print(Response(status=201, mimetype='application/json'),'для device_id',x,'добавлено')
                except (Exception, psycopg2.Error) as error:
                    print('Не удалось добавить данные в БД в endpoints, код ошибки', error)

        except (Exception, psycopg2.Error) as error:
            print('Не удалось добавить данные в БД в devices, код ошибки', error)

        finally:
            API3(cursor)
            close_connect(connect,cursor)
    return insert_db()
API2()

