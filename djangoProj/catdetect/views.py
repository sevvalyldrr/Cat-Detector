from django.shortcuts import redirect, render, get_object_or_404
from matplotlib.pyplot import gray
from .models import *
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
import numpy as np
import cv2

# Create your views here.


def index(request):
    url = request.META.get("HTTP_REFERER")
    current_user = request.user
    if request.method == "POST":
        images = request.FILES.getlist("images")
        for f in images:
            photo = Images(user_id=current_user.id, name="photo", images=f)
            photo.save()
        messages.success(request, "images added successfully")
        return HttpResponseRedirect(url)
    return render(request, "index.html")


def gallery(request):

    context = dict()
    current_user = request.user
    context["photos"] = Images.objects.filter(user_id=current_user.id)
    return render(request, "gallery.html", context)


def photo_detail(request, id):
    context = dict()
    current_user = request.user
    context["photo"] = get_object_or_404(Images, id=id, user_id=current_user.id)

    return render(request, "filter.html", context)


def cat_detection(request, id):
    image = Images.objects.get(id=id)
    image.save()

    if request.method == "POST":

        cat_cascade = cv2.CascadeClassifier(
            "/Users/sevvalyildirim/Desktop/djangoProj/cat.xml"
        )

        img = cv2.imread(image.images.path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cats = cat_cascade.detectMultiScale(gray, 1.1, 3)
        cats_num = len(cats)

        print("Cats detected: ", cats_num)
        messages.success(request, cats_num)

        q = Nums(
            cat_numbers=cats_num
        )
        q.save()

        return redirect("index2")
    return render(request, 'filter.html', locals())


def index2(request):
    result = []
    for i in Nums.objects.all():
        result.append(i)

    return render(request, "index2.html", locals())       
  


