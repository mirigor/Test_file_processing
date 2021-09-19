from file_processing.models import File
from django.shortcuts import render
import operator
import math
import os

tf = dict()
idf = dict()


def handle_uploaded_file(new_file):
    global tf, idf
    with open(f'files/test_file{new_file.id}.txt') as file:
        words = file.read()

        characters = ['\n', '.', ',', '!', '?', ':', ';']
        for character in characters:
            words = words.replace(f'{character}', '')  # удаление лишних символов
        words = words.split(' ')
        for word in words:  # приведение всех слов к нижнему регистру
            if not word.islower():
                words.append(word.lower())
                words.remove(word)

        list_of_unique_words = list(set(words))
        str_of_unique_words = " ".join(list_of_unique_words)  # строка уникальных слов из файла
        File.objects.filter(id=new_file.id).update(path_to_file=f'test_file{new_file.id}.txt',
                                                   words=str_of_unique_words)

        name_of_files = [name for name in os.listdir('files/') if
                         os.path.isfile(os.path.join('files/', name))]  # Имена файлов в папке

        if tf and idf:
            tf.clear()
            idf.clear()

        files_in_folder = []  # Список файлов находящихся в папке
        for f in name_of_files:
            files_in_folder.append(File.objects.get(path_to_file=f))

        for word in list_of_unique_words:  # Цикл по каждому слову
            count_of_files_with_a_word = 0

            for one_file in files_in_folder:
                if word in one_file.words:
                    count_of_files_with_a_word += 1
            tf[word] = (words.count(word) / len(words))
            idf[word] = math.log10(len(files_in_folder) / count_of_files_with_a_word)

        sorted_tuple = sorted(idf.items(), key=operator.itemgetter(1), reverse=True)  # сортировка словаря по значению
        idf = dict(sorted_tuple)
        file.close()


def upload_file(f, new_file):
    with open(f'files/test_file{new_file.id}.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    destination.close()


def index(request):
    global tf, idf
    if request.method == 'POST':
        new_file = File.objects.create()
        upload_file(request.FILES['file'], new_file)
        handle_uploaded_file(new_file)

        info_about_words = []
        if len(info_about_words):
            info_about_words.clear()

        for j, i in enumerate(idf):
            if j == 50:
                break
            info_about_words.append((i, tf[i], idf[i]))  # Объединение всей информации
        return render(request, 'index.html', {'info_about_words': info_about_words})

    return render(request, 'index.html', {})
