from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.views import View
from .models import room
@login_required(login_url='/login/')
def index(request):
    return render(request, 'ChatApp/index1.html',{'title' : 'Chat Room'})

def roomm(request, room_name):
    return render(request, 'ChatApp/room.html', {'room_name': room_name})

@login_required(login_url='/login/')
def p2pIndex(request):
    loggedin_user = request.user
    users = User.objects.filter(~Q(username=loggedin_user))
    user_list = [] 
    for each in users:
        user_list.append(each.username)
    
    return render(request, 'ChatApp/p2pindex.html',{'title' : 'Users','users' : user_list })

def p2pRoom(request,receiver):
    user = room.objects.create(user=receiver)
    user.save()
    return render(request, 'ChatApp/p2pRoom.html', {'room_name': 'room'})

# class p2pIndex(View):
   
#     @login_required(login_url='/login/')
#     def get(self, request):
#         loggedin_user = request.user
#         users = User.objects.filter(~Q(username=loggedin_user))
#         user_list = [] 
#         for each in users:
#             user_list.append(each.username)
    
#         return render(request, 'ChatApp/p2pindex.html',{'title' : 'Users','users' : user_list })

#     def post(self, request, *args, **kwargs):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             # <process form cleaned data>
#             return HttpResponseRedirect('/success/')

#         return render(request, self.template_name, {'form': form})

