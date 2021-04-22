from django.contrib.auth import login
from django.shortcuts import render, redirect

from .forms import UserRegisterForm
# Create your views here.

def regiser_view(request, *args, **kwargs):
    context={}
    form = UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(data = request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product_list')
    context['form']=form
    return render(request, 'registration/register.html', context=context)