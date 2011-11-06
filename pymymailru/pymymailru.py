# -*- coding: utf-8 -*-
"""
Created by Alexey Moskvin, 2011
"""

import hashlib
import urllib, urllib2

METHOD_GET = 'get'
METHOD_POST = 'post'

FORMAT_JSON = 'json'
FORMAT_XML = 'xml'

BASE_URL = u'http://www.appsmail.ru/platform/api?'

class ApiError:
    
    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __str__(self):
        return str(self.code) + ' ' + self.message

    def __unicode__(self):
        return unicode(self.code) + ' ' + self.message

class ApiCaller:

    def __init__(self, app_id, secret_key, format=FORMAT_JSON):
        self.app_id = app_id
        self.secret_key = secret_key
        self.format = format

    def __calc_signature(self, params):
        params_str = ''
        for key in sorted(params.iterkeys()):
            params_str += (key + '=' + params[key])
        return hashlib.md5(params_str + self.secret_key).hexdigest()

    def __prepare_api_params(self, format, method_name, params, session_key, uid):
        user_auth_param = None
        user_auth_data = None
        if session_key is not None and session_key != '':
            user_auth_param = 'session_key'
            user_auth_data = session_key
        elif uid is not None and uid != '':
            user_auth_param = 'uid'
            user_auth_data = uid
        api_params = {
            'method': method_name,
            'secure': 1,
            'format': format,
            'app_id': self.app_id,
            }
        if user_auth_param is not None:
            api_params[user_auth_param] = user_auth_data
        for param_name in params:
            api_params[param_name] = params[param_name]
            if api_params[param_name] is None:
                api_params[param_name] = ''
        for param in api_params:
            api_params[param] = unicode(api_params[param]).encode('utf-8')
        api_params['sig'] = self.__calc_signature(api_params)
        return api_params

    def __get_error_from_response(self, error_text, format):
        if format == FORMAT_JSON:
            import simplejson as json
            text = json.load(error_text)
            return ApiError(text['error']['error_code'], text['error']['error_msg'])
        else:
            from xml.dom import minidom
            text = minidom.parseString(error_text.read())
            code = text.getElementsByTagName('error_code')[0].firstChild.nodeValue
            msg = text.getElementsByTagName('error_msg')[0].firstChild.nodeValue
            return ApiError(code, msg)

    def execute(self, method_name, params, session_key_or_uid, format=FORMAT_JSON, method=METHOD_GET):
        if session_key_or_uid is not None:
            try:
                int(session_key_or_uid)
                session_key = None
                uid = unicode(session_key_or_uid)
            except ValueError:
                session_key = session_key_or_uid
                uid = None
            api_params = self.__prepare_api_params(format, method_name, params, session_key, uid)
        else:
            api_params = self.__prepare_api_params(format, method_name, params, None, None)
        if method == METHOD_GET:
            req = BASE_URL.encode('utf-8') + urllib.urlencode(api_params)
        else:
            req = urllib2.Request(BASE_URL, urllib.urlencode(api_params))
        try:
            result = urllib2.urlopen(req)
            return result.read()
        except urllib2.HTTPError, e:
            error = self.__get_error_from_response(e, format)
            raise error

class MyMailUtil:
    # Converts http://my.mail.ru/inbox/user/ to user@inbox.ru
    def link_to_email(self, link):
        if link is None:
            return None
        link = link[len('http://my.mail.ru/'):-1]
        parts = link.split('/')
        return parts[1] + '@' + parts[0] + '.ru'



class PyMyMailRu:

    def __split(self, l, n):
        return [l[i:i+n] for i in range(0, len(l), n)]


    def __init__(self, app_id, secret_key, format=FORMAT_JSON):
        self.app_id = app_id
        self.secret_key = secret_key
        self.format = format
        self.api_caller = ApiCaller(app_id, secret_key, format)

    def execute(self, method_name, params, session_key_or_uid, format=FORMAT_JSON, method=METHOD_GET):
        return self.api_caller.execute(method_name, params, session_key_or_uid, format, method)

    def audio_get(self, mids, uid, session_key):
        return self.execute('audio.get', {'mids' : mids, 'uid' : uid}, session_key, self.format)

    def audio_link(self, mid, session_key_or_uid):
        return self.execute('audio.link', {'mid' : mid}, session_key_or_uid, self.format)

    def audio_search(self, query, offset, limit, session_key_or_uid):
        return self.execute('audio.search', {'query' : query, 'offset' : offset, 'limit' : limit}, session_key_or_uid, self.format)

    def events_get_new_count(self, session_key_or_uid):
        return self.execute('events.getNewCount', {}, session_key_or_uid, self.format)

    def friends_get(self, ext, offset, session_key_or_uid):
        return  self.execute('friends.get', {'ext' : ext, 'offset' : offset}, session_key_or_uid, self.format)

    def friends_get_app_users(self, ext, offset, session_key_or_uid):
        return self.execute('friends.getAppUsers', {'ext' : ext, 'offset' : offset}, session_key_or_uid, self.format)

    def friends_get_invintations_count(self, uid, session_key):
        return self.execute('friends.getInvitationsCount', {'uid' : uid}, session_key, self.format)

    def guestbook_get(self, uid, offset, limit, session_key):
        return self.execute('guestbook.get', {'uid' : uid, 'offset' : offset, 'limit' : limit}, session_key, self.format)

    def guestbook_post(self, uid, title, description, user_text, img_url, img_file, link1_text, link1_href, link2_text, link2_href, session_key):
        return self.execute('guestbook.post', {'uid' : uid, 'title' : title, 'description' : description, 'user_text' : user_text,
                                               'img_url' : img_url, 'img_file' : img_file, 'link1_text' : link1_text,
                                                'link1_href' : link1_href, 'link2_text' : link2_text, 'link2_href' : link2_href,},
                            session_key, self.format)

    def mail_get_unread_count(self, session_key_or_uid):
        return self.execute('messages.getUnreadCount', {}, session_key_or_uid, self.format)

    def messages_get_thread(self, uid, offset, limit, session_key):
        return self.execute('messages.getThread', {'uid' : uid, 'offset' : offset, 'limit' : limit}, session_key, self.format)

    def messages_get_threads_list(self, uid, offset, limit, session_key):
        return self.execute('messages.getThreadsList', {'uid' : uid, 'offset' : offset, 'limit' : limit}, session_key, self.format)

    def messages_post(self, uid, message, session_key):
        return self.execute('messages.post', {'uid' : uid, 'message' : message}, session_key, self.format)

    def mobile_get_canvas(self, mobile_spec, session_key_or_uid):
        return self.execute('mobile.getCanvas', {'mobile_spec' : mobile_spec}, session_key_or_uid, self.format)

    def notifications_send(self, uids, text):
        return self.execute('notifications.send', {'uids' : uids, 'text' : text}, None, self.format, method=METHOD_POST)

    def photos_create_album(self, aid, title, description, privacy, password, session_key_or_uid):
        return self.execute('photos.createAlbum', {'aid' : aid, 'title' : title, 'description' : description,
                                                   'privacy' : privacy, 'password' : password},
                            session_key_or_uid, self.format, METHOD_POST)

    def photos_get(self, aid, pids, session_key_or_uid):
        return self.execute('photos.get', {'aid' : aid, 'pids' : pids}, session_key_or_uid, self.format)

    def photos_get_albums(self, aids, session_key_or_uid):
        return self.execute('photos.getAlbums', {'aids' : aids}, session_key_or_uid, self.format)

    def photos_upload(self, aid, img_url, img_file, name, description, tags, theme, session_key_or_id):
        return self.execute('photos.upload', {'aid' : aid, 'img_url' : img_url, 'img_file' : img_file, 'name' : name,
                                              'description' : description, 'tags' : tags, 'theme' : theme},
                            session_key_or_id, self.format)

    def stream_comment(self, thread_id, text, session_key_or_id):
        return self.execute('stream.comment', {'thread_id' : thread_id, 'text' : text}, session_key_or_id, self.format,
                            METHOD_POST)

    def stream_get(self, offset, limit, filter_app, session_key_or_id):
        return self.execute('stream.get', {'offset' : offset, 'limit' : limit, 'filrer_app' : filter_app}, session_key_or_id,
            self.format)

    def stream_get_by_author(self, uid, offset, limit, filter_app, session_key):
        return self.execute('stream.getByAuthor', {'uid' : uid, 'offset' : offset, 'limit' : limit, 'filter_app' : filter_app}
                            , session_key, self.format)

    def stream_like(self, thread_id, session_key_or_id):
        return self.execute('stream.like', {'thread_id' : thread_id}, session_key_or_id, self.format)

    def stream_post(self, user_text, text, title, link1_text, link1_href, link2_text, link2_href, img_url, session_key_or_id):
        return self.execute('stream.post', {'user_text' : user_text, 'text' : text, 'title' : title, 'link1_text' : link1_text,
                                            'link1_href' : link1_href, 'link2_text' : link2_text, 'link2_href' : link2_href,
                                            'img_url' : img_url}, session_key_or_id, self.format, METHOD_POST)

    def stream_share(self, url, description, title, img_url, user_text, session_key_or_uid):
        return self.execute('stream.share', {'url' : url, 'description' : description, 'title' : title, 'img_url' : img_url,
                                             'user_text' : user_text}, session_key_or_uid, self.format, METHOD_POST)

    def stream_unlike(self, thread_id, session_key_or_id):
        return self.execute('stream.unlike', {'thread_id' : thread_id}, session_key_or_id, self.format)

    def users_get_info(self, uids, session_key_or_uid):
        return  self.execute('users.getInfo', {'uids' : uids}, session_key_or_uid, self.format)


    def users_has_app_permission(self, ext_perm, session_key_or_uid):
        return  self.execute('hasAppPermission', {'ext_perm' : ext_perm}, session_key_or_uid, self.format)

    def users_is_app_user(self, session_key_or_uid):
        return  self.execute('users.isAppUser', {}, session_key_or_uid, self.format)


        