Описание
------------------------

PyMyMailRu - оболочка для REST-сервиса mail.ru (http://api.mail.ru/docs/guides/restapi/),
предназначенное для удобного доступа к нему с использованием языка Python. Позволяет вызывать методы
как если они были бы частью обычного Python-класса, скрывая транспорт и обработку ошибок.
На данный момент методы возвращают JSON или XML-строки, в будущем планируется типизация возвращаемых значений.


Установка
------------------------

Для использования скопируйте файл pymymailru.py в удобное место и импортируйте из него объекты PyMyMailRu и ApiError


Пример использования
------------------------

```python
# импорт
from pymymailru.pymymailru import PyMyMailRu, ApiError

# инициализация - передаем id приложения, секретный ключ и задаем формат выдачи
py_my_mail_ru = PyMyMailRu(123456, 'sf2u8jedfgdfglrjlht58', 'xml')
try:
    # получаем информацию о пользователе 1234567 от лица пользователя 7654321
    result = py_my_mail_ru.users_get_info(1234567, 7654321)
    print result
# обработка ошибок
except  ApiError, e:
    print e.code
    print e.message
```

Как видно, методы класса PyMyMailRu соответствуют методам из API mail.ru, единственным дополнительным параметром
является session_key_or_uid, показывающий для кого выполняется запрос.
Также присутствует метод execute, позволяющий сконструировать вызов к произвольному методу, указав его имя, параметры,
формат возвращаемых данных и метод запроса (GET/POST). Его можно использовать, если по какой-то причине не подходит
имеющийся вызов этого метода, например, изменились его параметры.


См. также
------------------------

http://api.mail.ru/docs/guides/restapi/
http://my.mail.ru/community/myplatform
