import os
from collections import Counter
source_tag = ''
# source_ini = os.path.join('d:', 'SLIV_PRJ', 'sliv.ini')
source_ini = os.path.join('d:', 'SLIV_PRJ', 'sliv4-utf8.ini')

print('{:=^120}'.format('ИСПРАВЛЕНИЕ ЗАПУЩЕНО'))
while not (source_tag == '1' or source_tag == '2'):
    source_tag = input('Укажите источник:\n 1: Облако mail.ru || 2: Диск D: ||   Введите 1/2:   ')
    if not (source_tag == '1' or source_tag == '2'):
        print('Неправильно указан источник: {}. Введите 1 или 2'.format(source_tag))
if source_tag == '1':
    source_dir = os.path.join('o:\\', '1')
else:
    source_dir = os.path.join('d:\\', '111')
print('source_dir = ', source_dir)


def read_ini(path): # считывает ini, заполняет массивы
    phase1 = False; phase2 = False; phase3 = False
    trash = [[], [], []]
    try:
        # f = open(path, 'r', encoding='cp1251')
        f = open(path, 'r', encoding='utf-8')
    except Exception:
        print('файл не открылся')
    for line in f:
        if line[:3] != '###' and line != '' and line != '\n':
            if line[:5] == '::::1':
                phase1 = True
                continue
            if line[:5] == '::::2':
                phase2 = True
                phase1 = False
                continue
            if line[:5] == '::::3':
                phase3 = True
                phase2 = False
                phase1 = False
                continue
            if phase3 and line[:5] == '::end':
                break
            if phase1:
                trash[0].append(line.rstrip('\n'))
            elif phase3:
                trash[2].append(line.rstrip('\n'))
            elif phase2:
                trash[1].append(line.rstrip('\n').split('::>::'))
    f.close()
    return trash

def consist_trash(name, shabl): # проверяет наличие трэша в имени
    c = False
    for i in shabl:
        if name.find(str(i)) != - 1:
            c = True
            break
    return c

def remove_trash(string, shabl):  # удаляет шаблоны из исходной строки
    for i in shabl:
        string = string.replace(str(i), '')
    return string

def is_trash_file(name, shabl):  # проверяет, является ли файл трешем, возвращает имя трешового файла
    c = ''
    for i,j in shabl:
        if name.find(str(i).strip()) != - 1:
            c = i
            break
    return c

# trash = read_ini(source_ini)
trash = read_ini(source_ini)

trashbox = list(trash[0])
trashfilesbox = list(trash[1])



tree = os.walk(source_dir, topdown=False, onerror=None, followlinks=False)

dirs_with_trash = 0
files_with_trash = 0
trashfiles_cnt = 0
trashfiles_arr =[]
longnames = []

for parent,dirs,files in tree:
    for i in dirs:
        # print('parent= {}\ndir= {}'.format(parent,d22))
        if consist_trash(i, trashbox):
            old= os.path.join(parent, i)
            new= os.path.join(parent, remove_trash(i, trashbox))
            os.rename(old, new)
            dirs_with_trash += 1
    for j in files:
        old = os.path.join(parent, j)
        lname = len(str(old))
        if lname < 260:
            if is_trash_file(j,trashfilesbox) != '':
                trashfiles_arr.append(j)
                os.remove(old)
                trashfiles_cnt += 1
            else:
                if consist_trash(j, trashbox):
                    new= os.path.join(parent,  remove_trash(j, trashbox))
                    os.rename(old, new)
                    files_with_trash += 1
        else:
            rec = [old, lname]
            longnames.append(rec)

print('{:=^120}'.format('ЗАВЕРШЕНО'))
# print('Завершено.\nИсправлено: {} директорий, {} файлов\nУдалено: {} трешовых файлов'.format(dirs_with_trash,files_with_trash,trashfiles_cnt))
print('Исправлено: {} директорий, {} файлов\nУдалено: {} трешовых файлов'.format(dirs_with_trash,files_with_trash,trashfiles_cnt))
if trashfiles_cnt !=0:
    print('{:=^120}'.format('ТРЕШОВЫЕ ФАЙЛЫ'))
for i,j in dict(Counter(trashfiles_arr)).items():
    print('Файл: {:<82}, {}'.format(i, j))
if longnames != []:
    print('{:=^120}'.format('ВНИМАНИЕ!'))
    print('{:=^120}'.format('Обнаружены и необработаны длинные имена:'))
    # print('ВНИМАНИЕ!\nОбнаружены и необработаны длинные имена:')
    for items in longnames:
        print(items)
print('{:=^120}'.format(''))






