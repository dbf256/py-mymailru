# -*- coding: utf-8 -*-
from pymymailru.pymymailru import PyMyMailRu, ApiError

py_my_mail_ru = PyMyMailRu(123456, 'rewrewsdf345345546546', 'xml')
try:
    result = py_my_mail_ru.users_get_info(1234567, 7654321)
    print result
except  ApiError, e:
    print e.code
    print e.message
