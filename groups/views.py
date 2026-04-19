from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Group, GroupMessage
from .forms import GroupForm, GroupMessageForm


@login_required
def group_list(request):
    my_groups = request.user.joined_groups.all()
    all_groups = Group.objects.exclude(members=request.user)
    return render(request, 'groups/group_list.html', {
        'my_groups': my_groups,
        'all_groups': all_groups,
    })


@login_required
def group_create(request):
    if request.method == 'POST':
        form = GroupForm(request.POST, request.FILES)
        if form.is_valid():
            group = form.save(commit=False)
            group.creator = request.user
            group.save()
            group.members.add(request.user)
            messages.success(request, f'Group "{group.name}" created!')
            return redirect('group_detail', group_id=group.id)
    else:
        form = GroupForm()
    return render(request, 'groups/group_form.html', {'form': form, 'action': 'Create'})


@login_required
def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    is_member = request.user in group.members.all()
    group_messages = group.messages.select_related('user').all()
    msg_form = GroupMessageForm()

    if request.method == 'POST' and is_member:
        msg_form = GroupMessageForm(request.POST)
        if msg_form.is_valid():
            gm = msg_form.save(commit=False)
            gm.group = group
            gm.user = request.user
            gm.save()
            return redirect('group_detail', group_id=group.id)

    return render(request, 'groups/group_detail.html', {
        'group': group,
        'is_member': is_member,
        'group_messages': group_messages,
        'msg_form': msg_form,
    })


@login_required
def join_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    group.members.add(request.user)
    messages.success(request, f'Joined "{group.name}"!')
    return redirect('group_detail', group_id=group.id)


@login_required
def leave_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    group.members.remove(request.user)
    messages.info(request, f'Left "{group.name}".')
    return redirect('group_list')