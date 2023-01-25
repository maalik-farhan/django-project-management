from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Project, Tag
from django.contrib import messages
from .forms import ProjectForm, ReviewForm
from .utils import searchProjects, paginationProjects


# Create your views here.


def projects(request):

    data, search_query = searchProjects(request)
    custom_range, data = paginationProjects(request, data, 6)
    context = {"data": data, 'search_query': search_query, 'custom_range': custom_range}
    return render(request, 'users/projects.html', context)


def project(request, pk):
    project_obj = Project.objects.get(id=pk)
    form = ReviewForm()
    tags = project_obj.tags.all()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = project_obj
        review.owner = request.user.profile
        review.save()

        project_obj.getVoteCount()

        messages.success(request, 'Your review was successfully submitted!')

        return redirect('project', pk=project_obj.id)

    return render(request, 'users/single-project.html', {'project': project_obj, 'tags': tags, 'form': form})


@login_required(login_url="login")
def create_project(request):
    profile = request.user.profile
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            newtags = request.POST.get('newtags').replace(",", ' ').split()
            project = form.save(commit=False)
            project.owner = profile
            project.save()

            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('projects')
    context = {'form': form}
    return render(request, 'users/project_form.html', context)


@login_required(login_url="login")
def update_project(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)
    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(",", ' ').split()
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('account')
    context = {'form': form, 'project': project}
    return render(request, 'users/project_form.html', context)


@login_required(login_url="login")
def delete_project(request, pk):
    profile = request.user.profile

    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()

        return redirect('projects')
    context = {'project': project}
    return render(request, 'delete_template.html', context)
