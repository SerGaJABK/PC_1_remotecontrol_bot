Данный проект представляет собой разработку Telegram-бота с различными функциями, включая получение IP-адреса, отображение характеристик системы, захват скриншотов, использование веб-камеры, отправку сообщений на экран, установку обоев рабочего стола, выключение и перезагрузку компьютера.

Регистрация бота
Прежде чем запустить bot_run.py нужно зарегистрировать у @BotFather, чтобы получить токен (ключ) для работы с Telegram API.
Зайти в Telegram и набрать в поисковой строке @BotFather. Отправить ему /newbot. Перейти в него, нажать кнопку Старт / Запустить бота, а затем выбрать в меню слева или ввести в строке сообщения команду /newbot— первый шаг к регистрации бота. 
Следующим шагом, нужно придумать имя бота. Разрешено вводить как на русском, так и на английском языке. Потом, следует выбрать имя пользователя бота. Имя пользователя будет являться частью ссылки, начинающейся с t.me и заканчивающейся тем, что выбрать в качестве имени. 


Когда придумано имя бота и имя пользователя, BotFather автоматически создаст токен нового бота — это строка из символов, которая авторизует бота и подтверждает его подлинность при добавлении в конструкторы и иные сервисы управления готовыми ботами. Понадобятся токен нового бота и id.

Для инициализации и настройки Telegram-бота подключается токен бота в файле bot_run.py, API-ключ, CHAT_ID, показано на рисунке 5. CHAT_ID можно найти в Telegram-боте @ShowJsonBot. Вписываем это значение в файл bot_run.py в переменную CHAT_ID

