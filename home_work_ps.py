#!/usr/bin/env python3
import sys
import subprocess
from datetime import datetime
from collections import Counter



def get_time_now():
    """Возвращает текущее время в формате 'дд.мм.ГГГГ_ЧЧ:ММ:СС'.

    Returns:
        str: Строка с текущей датой и временем.
    """
    now = datetime.now()
    time_now = now.strftime("%d.%m.%Y_%H:%M:%S")
    return time_now

def parse_ps_aux():
    """Парсит вывод команды 'ps aux' и возвращает статистику по процессам.

    Собирает данные о пользователях, использовании CPU и RAM, а также находит
    процессы с максимальной нагрузкой.

    Returns:
        tuple: Кортеж с собранной статистикой в формате:
            (
                list: Уникальные пользователи (list[str]),
                list: Все процессы (list[str]),
                float: Суммарное использование RAM (%),
                float: Суммарное использование CPU (%),
                str: Процесс с максимальным использованием RAM,
                str: Процесс с максимальным использованием CPU,
                dict: Количество процессов по пользователям ({user: count})
            )
    """
    list_users = []
    list_memory_usage = []
    list_cpu_usage = []
    sum_memory_usage = 0
    sum_cpu_usage = 0
    max_poc_cpu = ''
    max_poc_mem = ''


    result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)

    processes = result.stdout.splitlines()

    max_number_cpu = float(processes[1].split()[2])
    max_number_mem = float(processes[1].split()[3])

    for line in processes[1:]:
        parts = line.split()
        user = parts[0]
        cpu_usage = float(parts[2])
        mem_usage = float(parts[3])
        proc_name = parts[10]

        list_users.append(user)

        list_memory_usage.append(mem_usage)
        if float(mem_usage) > max_number_mem:
            max_number_mem = float(mem_usage)
            max_poc_mem = proc_name

        list_cpu_usage.append(cpu_usage)
        if float(cpu_usage) > max_number_cpu:
            max_number_cpu = float(cpu_usage)
            max_poc_cpu = proc_name

    users = list(set(list_users))

    num_proc_user = dict(Counter(list_users))

    for mem_use in list_memory_usage:
        sum_memory_usage += float(mem_use)

    for cpu_use in list_cpu_usage:
        sum_cpu_usage += float(cpu_use)

    return users, processes, sum_memory_usage, sum_cpu_usage, max_poc_mem, max_poc_cpu, num_proc_user

def main():
    """Генерирует и сохраняет отчёт о состоянии системы в файл.

    Основной поток выполнения:
    1. Получает текущее время для имени файла
    2. Собирает статистику процессов через parse_ps_aux()
    3. Сохраняет отчёт в файл system_report_<время>.txt
    4. Восстанавливает стандартный вывод

    Отчёт включает:
    - Список пользователей системы
    - Общее количество процессов
    - Количество процессов по пользователям
    - Суммарное использование памяти и CPU
    - Процессы с максимальным потреблением ресурсов
    """
    time_now = get_time_now()
    users, processes, sum_memory_usage, sum_cpu_usage, max_poc_mem, max_poc_cpu, num_proc_user = parse_ps_aux()
    with open(f"system_report_{time_now}.txt", "w") as f:
        sys.stdout = f
        print("Отчёт о состоянии системы:", end='\n')
        print(f"Пользователи системы: {users}", end='\n')
        print(f"Процессов запущено: {len(processes)}", end='\n\n')
        print("Пользовательских процессов:", end="\n")
        for k, v in num_proc_user.items():
            print(k, ": ", v)
        print()
        print(f"Всего памяти используется: {sum_memory_usage}%")
        print(f"Всего CPU используется: {sum_cpu_usage}%")
        print(f"Больше всего памяти использует: {max_poc_mem[:20]}")
        print(f"Больше всего CPU использует: {max_poc_cpu[:20]}")
        sys.stdout = sys.__stdout__

    print("Отчёт сохранён в system_report.txt")

if __name__ == "__main__":
    main()