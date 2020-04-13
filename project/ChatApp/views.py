from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.views import View
from .models import room
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView



class p2pRoom(APIView):
    
    def get(self,request):
        
        loggedin_user = request.user
        receiver=request.GET.get('receiver')
        
        if receiver is not None:
            user = room.objects.create(user=receiver)
            user.save()

        users = User.objects.filter(~Q(username=loggedin_user))
        user_list = [] 
        for each in users:
            user_list.append(each.username)
        return render(request, 'ChatApp/chatapp.html', {'room_name': 'room','users' : user_list ,'sender': loggedin_user})
    
   
        
@login_required(login_url='/login/',redirect_field_name='/chat/')
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
    
    #return render(request, 'ChatApp/p2pindex.html',{'title' : 'Users','users' : user_list })
    return render(request, 'ChatApp/chatapp.html',{'title' : 'Users','users' : user_list })

   
# def p2pRoom(request,receiver):
#     #user = room.objects.create(user=receiver)
#     #user.save()
#     loggedin_user = request.user
#     users = User.objects.filter(~Q(username=loggedin_user))
#     user_list = [] 
#     for each in users:
#         user_list.append(each.username)
#     return render(request, 'ChatApp/chatapp.html', {'room_name': 'room','users' : user_list })

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






# @login_required(login_url='/login/')
# def p2pIndex(request):
#     loggedin_user = request.user
#     users = User.objects.filter(~Q(username=loggedin_user))
#     user_list = [] 
#     for each in users:
#         user_list.append(each.username)
    
#     #return render(request, 'ChatApp/p2pindex.html',{'title' : 'Users','users' : user_list })
#     return render(request, 'ChatApp/chatapp.html',{'title' : 'Users','users' : user_list })

# def p2pRoom(request,receiver):
#     user = room.objects.create(user=receiver)
#     user.save()
#     return render(request, 'ChatApp/chatapp.html', {'room_name': 'room'})


