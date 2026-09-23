import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
import random
import time

print('*' * 25)
print('Приветствую тебя в игре на знание иностранных языков!✋')
print('Программа будет называть слова на русском, а тебе нужно переводить их голосом.🗣')
print('*' * 25)

errors = 0
points = 0
max_errors = 3
duration = 4
sample_rate = 44100

languages_dict = {
    "английский": "en-US",
    "испанский": "es-ES",
    "португальский": "pt-PT",
    "индонезийский": "id-ID",
    "польский": "pl-PL",
    "итальянский": "it-IT",
    "турецкий": "tr-TR"
}

multilang_vocabulary = {
    "кот": ["cat", "gato", "gato", "kucing", "kot", "gatto", "kedi"],
    "собака": ["dog", "perro", "cachorro", "anjing", "pies", "cane", "köpek"],
    "яблоко": ["apple", "manzana", "maçã", "apel", "jabłko", "mela", "elma"],
    "молоко": ["milk", "leche", "leite", "susu", "mleko", "latte", "süt"],
    "солнце": ["sun", "sol", "sol", "matahari", "słońce", "sole", "güneş"],
    "банан": ["banana", "plátano", "banana", "pisang", "banan", "banana", "muz"],
    "школа": ["school", "escuela", "escola", "sekolah", "szkoła", "scuola", "okul"],
    "друг": ["friend", "amigo", "amigo", "teman", "przyjaciel", "amico", "arkadaş"],
    "окно": ["window", "ventana", "janela", "jendela", "okno", "finestra", "pencere"],
    "жёлтый": ["yellow", "amarillo", "amarelo", "kuning", "żółty", "giallo", "sarı"],
    "технология": ["technology", "tecnología", "tecnologia", "teknologi", "technologia", "tecnologia", "teknoloji"],
    "университет": ["university", "universidad", "universidade", "universitas", "uniwersytet", "università", "üniversite"],
    "информация": ["information", "información", "informação", "informasi", "informacja", "informazione", "bilgi"],
    "произношение": ["pronunciation", "pronunciación", "pronúncia", "pengucapan", "wymowa", "pronuncia", "telaffuz"],
    "воображение": ["imagination", "imaginación", "imaginação", "imajinasi", "wyobraźnia", "immaginazione", "hayal gücü"]
}

words_by_level = {
    "easy": ["кот", "собака", "яблоко", "молоко", "солнце"],
    "medium": ["банан", "школа", "friend", "окно", "жёлтый"],
    "hard": ["технология", "университет", "информация", "произношение", "воображение"]
}

recognizer = sr.Recognizer()

print("\nДоступные языки для изучения:")
for lang in languages_dict.keys():
    print(f"- {lang.capitalize()}")

user_input = input("\nНа каком языке ты будешь отвечать? (английский, испанский, португальский и др.): ").lower().strip()

selected_lang = None
for lang, code in languages_dict.items():
    if user_input in lang or user_input in code.lower() or lang[:4] in user_input:
        selected_lang = lang
        break

if selected_lang in languages_dict:
    lang_code = languages_dict[selected_lang]
    lang_index = list(languages_dict.keys()).index(selected_lang)
    
    level = input("Введите сложность (easy, medium, hard): ").lower().strip()
    
    if level in words_by_level:
        selected_words = words_by_level[level].copy()
        random.shuffle(selected_words)
        
        print(f"\nИгра началась! Выбран язык: {selected_lang.capitalize()}. Поехали!")
        
        for word in selected_words:
            if errors >= max_errors:
                print("\nИгра окончена!😭 Достигнут лимит ошибок. Попробуйте снова")
                break
                
            print(f"\nКак переводится слово: {word.upper()}?")
            print('Приготовься...')
            print('3')
            time.sleep(1)
            print('2')
            time.sleep(1)
            print('1')
            time.sleep(1)
            print("ГОВОРИ!")
            
            recording = sd.rec(
                int(duration * sample_rate),
                samplerate=sample_rate,
                channels=1,
                dtype="int16"
            )
            sd.wait()
            
            print("Запись завершена. Проверяю...")
            wav.write("temp_output.wav", sample_rate, recording)
            
            with sr.AudioFile("temp_output.wav") as source:
                audio = recognizer.record(source)
                
            try:
                text = recognizer.recognize_google(audio, language=lang_code).lower().strip()
                print("Ты сказал:", text)
                
                correct_answer = multilang_vocabulary[word][lang_index]
                
                if text == correct_answer.lower():
                    print("Правильно! 🎉")
                    points += 1
                else:
                    print(f"Неверно. ❌ Правильный ответ: {correct_answer}")
                    errors += 1
            except sr.UnknownValueError:
                print("Не удалось распознать речь. Засчитана ошибка.")
                errors += 1
            except sr.RequestError as e:
                print(f"Ошибка сервиса: {e}")
                errors += 1
                
            time.sleep(1.5)
    else:
        print("Неверный уровень сложности. Выберите easy, medium или hard.")
else:
    print("Такой язык пока не поддерживается.")

print('\n' + '=' * 25)
print('ПОДВЕДЕМ ИТОГИ:')
print(f"Ваши очки: {points}")
print(f"Ошибки: {errors} из {max_errors}")
print('=' * 25)