from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Message
from accounts.models import User


@login_required
def chat_list(request):
    # Get all users who have chatted with current user
    sent = Message.objects.filter(sender=request.user).values_list('receiver_id', flat=True)
    received = Message.objects.filter(receiver=request.user).values_list('sender_id', flat=True)
    chat_user_ids = set(list(sent) + list(received))
    chat_users = User.objects.filter(id__in=chat_user_ids).exclude(id=request.user.id)
    all_users = User.objects.exclude(id=request.user.id)
    return render(request, 'chat/chat.html', {
        'chat_users': chat_users,
        'all_users': all_users,
        'active_chat': None,
    })


@login_required
def chat_room(request, receiver_id):
    receiver = get_object_or_404(User, id=receiver_id)
    messages = Message.objects.filter(
        Q(sender=request.user, receiver=receiver) |
        Q(sender=receiver, receiver=request.user)
    ).order_by('timestamp')

    # Mark messages as read
    messages.filter(receiver=request.user, is_read=False).update(is_read=True)

    sent = Message.objects.filter(sender=request.user).values_list('receiver_id', flat=True)
    received = Message.objects.filter(receiver=request.user).values_list('sender_id', flat=True)
    chat_user_ids = set(list(sent) + list(received))
    chat_user_ids.add(receiver.id)
    chat_users = User.objects.filter(id__in=chat_user_ids).exclude(id=request.user.id)
    all_users = User.objects.exclude(id=request.user.id)

    return render(request, 'chat/chat.html', {
        'chat_users': chat_users,
        'all_users': all_users,
        'receiver': receiver,
        'messages': messages,
        'active_chat': receiver,
    })