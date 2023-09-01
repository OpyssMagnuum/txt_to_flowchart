def enter_scheme(sh_print, read_from):
    with open(read_from, encoding="utf-8",
              mode="r") as f:
        lines = [line.rstrip() for line in f]  # делим линии
    if sh_print:
        for i in range(len(lines)):
            print(lines[i])
    f.close()
    return lines


def enter_specific(num, prntout, read_from):
    # print(read_from)
    with open(read_from, encoding="utf-8",
              mode="r") as f:
        lines = [line.rstrip() for line in f]
        if prntout:
            print(lines[num])
    f.close()
    return lines[num]


def find_Main(spisok):  # ищем основные элементы(те что с циферкой)
    arr = []
    for i in range(len(spisok)):
        if len(spisok[i].strip()) > 0 and spisok[i][0].isdigit():
            # print(list[i])
            arr.append(spisok[i])
    return arr


def find_Extra(spisok, read_from):  # ищем доп. элементы(те что без циферок)
    arr = []  # список в который заполним все доп элементы
    ex = 0  # цифра, идущая после точки: 1.>2< / 3.>1<
    save = -1  # проверка на разрыв, если есть, то первая цифра меняется(чтобы менялось с 1.1 на 2.1 и тд)
    main_index = 0  #
    for i in range(len(spisok)):
        if len(spisok[i].strip()) > 0 and not spisok[i][0].isdigit():
            if save + 1 != i:  # проверка на разрыв
                main_index = i - 1  # если разрыв есть, то элемент до - основной
                ex = 1
            arr.append(get_str_num(enter_specific(main_index, False, read_from))
                       + "." + str(ex) + " " + spisok[i])
            save = i
            ex += 1
    return arr


def get_str_num(stroka):  # ищем число в начале(ТОЛЬКО У ОСНОВНЫХ ЭЛЕМЕНТОВ)
    num = ""
    for i in range(len(stroka)):
        if not (stroka[i].isdigit()) and (
                i != 0):
            break
        num += str(stroka[i])
    return num


def razdel(s, n):  # функция делит строку на {\n} с лимитом n
    words = s.split()
    result = ""
    count = 0
    for word in words:
        if count + len(word) > n:
            result += "\n" + word + " "
            count = len(word) + 1
        else:
            result += word + " "
            count += len(word) + 1
    return result.strip()
