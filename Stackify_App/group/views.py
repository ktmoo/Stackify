from django.shortcuts import render
from django.shortcuts import render,redirect,HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponseBadRequest,Http404
from django.contrib.auth.decorators import login_required
from . forms import GroupForm
from .models import Group



@login_required
def create_a_group(request):
    form=GroupForm(request.POST or None)
    if form.is_valid():
        group=form.save(commit=False)
        group.owner=request.user
        group.save()
        form=GroupForm(None)
        return redirect('groups')
    context={"form": form}
    return render(request,'group/create_group.html',context)


def groups(request):
    groups=Group.objects.all()
    return render(request,'group/groups.html',{"groups": groups})