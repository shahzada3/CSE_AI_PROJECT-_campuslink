from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project, Task
from .forms import ProjectForm, TaskForm


@login_required
def project_list(request):
    my_projects = request.user.joined_projects.all() | request.user.created_projects.all()
    my_projects = my_projects.distinct()

    explore = Project.objects.exclude(members=request.user).exclude(creator=request.user)

    return render(request, 'projects/project_list.html', {
        'my_projects': my_projects,
        'explore': explore,
    })


@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.creator = request.user
            project.save()
            project.members.add(request.user)
            messages.success(request, f'Project "{project.name}" created!')
            return redirect('project_detail', project_id=project.id)
    else:
        form = ProjectForm()

    return render(request, 'projects/project_form.html', {
        'form': form,
        'action': 'Create'
    })


@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    is_member = request.user in project.members.all() or request.user == project.creator

    tasks = project.tasks.select_related('assigned_to').all()
    task_form = TaskForm(project=project)

    if request.method == 'POST' and is_member:
        task_form = TaskForm(request.POST, project=project)
        if task_form.is_valid():
            task_form.save()
            return redirect('project_detail', project_id=project.id)

    return render(request, 'projects/project_detail.html', {
        'project': project,
        'is_member': is_member,
        'tasks': tasks,
        'task_form': task_form,
    })


@login_required
def join_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    project.members.add(request.user)
    messages.success(request, f'Joined project "{project.name}"!')
    return redirect('project_detail', project_id=project.id)


@login_required
def toggle_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.is_done = not task.is_done
    task.save()
    return redirect('project_detail', project_id=task.project.id)