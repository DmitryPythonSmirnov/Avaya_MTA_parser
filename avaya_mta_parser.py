'''
Скрипт парсит файл MTA-файл (файл, полученный с помощью MTA (Message Trace Analyzer)
из MST (Message Sequence Trace)) от станции Avaya для вызовов по SIP-транку.
Скрипт запрашивает номер телефона вызывающего абонента (From) или Call-ID вызова.
Если введён номер телефона, то будет найден только первый вызов в файле
с этим номером (скрипт сам найдёт Call-ID этого вызова).
Собирает все SIP-сообщения с соответствующим Call-ID в файл "result.txt".

Версия от 2022-10-14.
'''

import os
import re
import sys


RESULT_FILE = 'result.txt'


###############################################################################
#                          Функция get_parse_criteria                         #
###############################################################################
def get_parse_criteria():
    '''
    Получить критерий парсинга
    '''
    answer = input('Выберите критерий парсинга:\n'
        '[1] Парсинг по номеру вызывающего абонента (From)\n'
        '[2] Парсинг по Call-ID\n'
        'Выбор: ')

    return answer


###############################################################################
#                           Функция get_file_number                           #
###############################################################################
def get_file_number(file_list):
    '''
    Вернуть номер файла для парсинга
    '''
    for number, file in enumerate(file_list):
        print(f'[{number + 1}] {file}')
    
    while True:
        file_number = input('Введите номер файла для парсинга. Для выхода введите q: ')
        if file_number == 'q':
            break
        if not file_number.isdigit():
            print('Вы ввели не число')
        elif int(file_number) > len(file_list):
            print('Нет такого файла')
        else:
            return int(file_number)


###############################################################################
#                           Функция get_next_block                            #
###############################################################################
def get_next_block(file_obj):
    '''
    Получить следущий блок текста из файла
    '''
    block = []
    blank_lines_count = 0
    for line in file_obj:
        block.append(line)
        if line == '\n':
            if blank_lines_count == 0:
                blank_lines_count += 1

            elif blank_lines_count == 1:
                blank_lines_count = 0
                return block
            else:
                raise ValueError('Неправильный подсчёт blank_lines_count')
        else:
            blank_lines_count = 0
    
    return None


###############################################################################
#                      Функция get_phone_number_and_call_id                   #
###############################################################################
def get_phone_number_and_call_id(file_name, phone_number):
    '''
    Найти строку с полным номером в файле,
    и Call-ID для этого вызова
    '''
    with open(file_name) as f:
        while True:
            block = get_next_block(f)
            if not block:
                # Конец файла
                return None, None
            for line in block:
                if re.search(f'^From: .*:\d*{phone_number}\d*@', line):
                    for line2 in block:
                        if line2.startswith('Call-ID:'):
                            call_id = line2[9:].strip()
                    return line, call_id


###############################################################################
#              Функция проверки наличия call_id в блоке текста                #
###############################################################################
def check_call_id_in_block(block, call_id):
    '''
    Есть ли call_id в блоке текста
    '''
    for line in block:
        if re.search(call_id, line):
            return True
    return False


###############################################################################
#                        Функция парсинга файла по call_id                    #
###############################################################################
def parse_file(file_name, call_id):
    with open(file_name) as f1:
        with open(RESULT_FILE, 'w') as f2:
            while True:
                block = get_next_block(f1)
                # Если блок не найден (конец файла), то выходим из цикла
                if not block:
                    break

                if check_call_id_in_block(block, call_id):
                    for line in block:
                        f2.write(line)


###############################################################################
#                           Функция выхода из скрипта                         #
###############################################################################
def exit_func():
    input('Для выхода нажмите Enter...')
    sys.exit(0)


###############################################################################
#                                Main function                                #
###############################################################################
def main():
    file_list = os.listdir()

    # Выбор файла для парсинга
    file_number = get_file_number(file_list)

    if not file_number:
        exit_func()
        
    file_name = file_list[file_number - 1]

    # Выбор критерия парсинга - по номеру или по Call_ID
    parse_criteria = get_parse_criteria()

    if parse_criteria == '1':
        phone_number_input = input('Введите номер (или часть номера) вызывающего абонента (From): ')
        line_with_phone_number, call_id = get_phone_number_and_call_id(file_name, phone_number_input)
        
        if line_with_phone_number is None:
            print('Ничего не найдено')
            exit_func()
        
        answer = input(f'В строке ниже указан правильный номер?\n{line_with_phone_number} (y/n) [y]: ')
        if not (answer.lower() == 'y' or answer == ''):
            # Выход из скрипта
            exit_func()

    
    elif parse_criteria == '2':
        call_id = input('Введите Call-ID: ')

    else:
        print('Вы ввели недопустимый вариант')
        exit_func()

    # Обработка файла
    parse_file(file_name, call_id)
    print('Обработка файла завершена.')
    exit_func()


###############################################################################
#                             Launch the script                               #
###############################################################################  
if __name__ == '__main__':
    main()
