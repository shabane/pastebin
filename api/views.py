import json
from django.http.response import JsonResponse
from django.shortcuts import render
from clipboard.models import User, Clipboard
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse
from clipboard import views as utils
from hashlib import blake2b

def AddText(request):
    user = request.GET['user']
    password = request.GET['password']
    text = request.GET['text']
    user = User.objects.filter(username=user)
    if(user):
        if(check_password(password, user[0].password)):
            Clipboard.objects.create(author=user[0], text=text)
            return JsonResponse({
                'result': True,
                'msg': 'text added'
            })
        else:
            return JsonResponse({
                'result': False,
                'msg': 'username or password incorrect'
            })
    else:
        return JsonResponse({
                'result': False,
                'msg': 'username or password incorrect'
            })


def UserLogin(request):
    user = request.GET['user']
    password = request.GET['password']
    user = User.objects.filter(username=user)
    if(user):
        if(check_password(password, user[0].password)):
            return JsonResponse({
                'result': True,
                'msg': 'username and password maches'
            })
        else:
            return JsonResponse({
                'result': False,
                'msg': 'username or password incorect'
            })
    else:
        return JsonResponse({
                'result': False,
                'msg': 'username or password incorect'
            })


def DeleteText(request):
    user = request.GET['user']
    password = request.GET['password']
    textId = request.GET['id']
    user = User.objects.filter(username=user)
    if(user):
        if(check_password(password, user[0].password)):
            if(Clipboard.objects.filter(id=textId, author=user[0]).delete()[0] == 1):
                return JsonResponse({
                'result': True,
                'msg': 'object deleted'
            })
            else:
                return JsonResponse({
                'result': False,
                'msg': 'object not found'
            })
        else:
            return JsonResponse({
                'result': False,
                'msg': 'username or password incorrect'
            })
    else:
        return JsonResponse({
                'result': False,
                'msg': 'username or password incorrect'
            })


def ShareText(request):
    user = request.GET['user']
    password = request.GET['password']
    textId = request.GET['id']
    user = User.objects.filter(username=user)
    if(user):
        if(check_password(password, user[0].password)):
            clipb = Clipboard.objects.filter(pk=textId, author=user[0])
            if(clipb):
                if(not clipb[0].link):
                    link = blake2b(clipb[0].text.encode('utf-8'), digest_size=3).hexdigest()
                    clipb.update(link=link)
                    return JsonResponse({
                        'result': True,
                        'link': link
                    })
                else:
                    return JsonResponse({
                        'result': True,
                        'link': clipb[0].link
                    })
            else:
                return JsonResponse({
                        'result': False,
                        'msg': 'object not found'
                    })
        else:
            return JsonResponse({
                'result': False,
                'msg': 'username or password incorrect'
            })
    else:
        return JsonResponse({
                'result': False,
                'msg': 'username or password incorrect'
            })


def CheckChanges(request):
    user = request.GET['user']
    password = request.GET['password']
    user = User.objects.filter(username=user)
    if(user):
        if(check_password(password, user[0].password)):
            texts_id = []
            for i in Clipboard.objects.filter(author=user[0]):
                texts_id.append(i.id)
            return JsonResponse({
                'result': True,
                'TextsId': texts_id,
                'msg': None
                })
        else:
            return JsonResponse({
                'result': False,
                'msg': 'username or password incorrect'
            })
    else:
        return JsonResponse({
                'result': False,
                'msg': 'username or password incorrect'
            })


def GetText(request):
    user = request.GET['user']
    password = request.GET['password']
    user = User.objects.filter(username=user)
    lst = request.GET.getlist('id')
    if(user):
        if(check_password(password, user[0].password)):
            clipb = []
            for i in lst:
                if(j := Clipboard.objects.filter(author=user[0], pk=int(i))):
                    clipb.append({
                        'status': 1,
                        'text': j[0].text,
                        'id': j[0].id,
                        'link': j[0].link
                    })
                else:
                    clipb.append({
                        'status': 0,
                        'msg': 'object ' + i + ' not exist'
                    })
            return JsonResponse({'result': True, 'objects': clipb})
        else:
            return HttpResponse('username or password incorrect')
    else:
        return HttpResponse('username or password incorrect')


