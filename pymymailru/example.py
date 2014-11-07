# импорт
from pymymailru import PyMyMailRu, ApiError

# инициализация - передаем id приложения, секретный ключ и задаем формат выдачи
py_my_mail_ru = PyMyMailRu(123456, 'sf2u8jedfgdfglrjlht58', 'xml')
try:
    # получаем информацию о пользователях 1234567, 1234568 от лица пользователя 7654321
    result = py_my_mail_ru.users_get_info('1234567,1234568', 7654321)
    print result
# обработка ошибок
except ApiError, e:
    print e.code
    print e.message
