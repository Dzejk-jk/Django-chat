"""
This file contains the views for the chat application.
"""
from django.shortcuts import render, redirect
from chat.models import Room, Message
from django.http import HttpResponse, JsonResponse


def home(request):
    """
    This function returns the home page for the chat application.
    """
    return render(request, 'home.html')


def room(request, room):
    """
    This function returns the room page for the chat application.
    """
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html', {
        'room': room,
        'username': username,
        'room_details': room_details,
    })


def checkview(request):
    """
    This function checks if the room exists, and if it does not, creates a new room.
    """
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room).exists():
        return redirect('/' + room + '/?username=' + username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/' + room + '/?username=' + username)


def send(request):
    """
    This function sends a message to the room.

    Returns:
        HttpResponse: An HTTP response indicating that the message was sent.
    """
    message = request.POST['message']
    user_name = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, 
                                         user=user_name, 
                                         room=room_id)
    new_message.save()
    return HttpResponse('Message sent')


def getMessages(request, room):
    """
    This function returns the messages for a given room.

    Parameters:
        request (HttpRequest): The incoming request.
        room (str): The name of the room.

    Returns:
        JsonResponse: A JSON response containing the messages for the room.
    """
    room_details = Room.objects.get(name=room)
    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({'messages': list(messages.values())})