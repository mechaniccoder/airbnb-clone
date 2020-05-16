from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django_countries import countries
from django.views.generic import ListView, DetailView, UpdateView, CreateView, FormView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator
from users import mixins as user_mixins
from . import models
from . import forms

""" FUCTION BASED VIEW

def all_rooms(request):
    page = request.GET.get("page", 1)
    print(page)
    room_list = models.Room.objects.all()  # 쿼리셋이지만 아직 불러온게 아니라서 데이터베이스를 죽이지않음
    paginator = Paginator(room_list, 10, orphans=5)

    # get_page() 메소드를 이용한 경우(get_page는 page objects를 return한다.)
    # rooms = paginator.get_page(page)
    # return render(request, "rooms/home.html", context={"pages": rooms,})

    # page() 메소드를 이용한 경우(page()는 page objects를 return한다. get_page()와 같지만 유효성 검사를 하지 않지 않는다.
    try:
        rooms = paginator.page(int(page))
        return render(request, "rooms/home.html", context={"pages": rooms},)

    except EmptyPage:  # 빈 페이지 error
        return redirect("/")
"""


class HomeView(ListView):
    model = models.Room
    paginate_by = 12
    ordering = "created"
    paginate_orphans = 5
    context_object_name = "rooms"


# def room_detail(request, pk):

#     try:
#         room = models.Room.objects.get(pk=pk)
#         return render(request, "rooms/detail.html", context={"room": room})

#     except models.Room.DoesNotExist:
#         raise Http404()


class RoomDetail(DetailView):

    """ DetailView는 자동으로 pk인자를 찾고 object를 찾지못하면
    자동으로 404페이지를 return한다. """

    model = models.Room


def search(request):
    country = request.GET.get("country")

    if country:
        # country key에 대한 value가 존재하면 정보가 입력된 form을 보여준다.
        form = forms.SearchForm(request.GET)
        # form 안에서 에러와 같은 것이 있는지 확인한다.
        if form.is_valid():
            city = form.cleaned_data.get("city")
            country = form.cleaned_data.get("country")
            room_type = form.cleaned_data.get("room_type")
            price = form.cleaned_data.get("price")
            guests = form.cleaned_data.get("guests")
            bedrooms = form.cleaned_data.get("bedrooms")
            beds = form.cleaned_data.get("beds")
            baths = form.cleaned_data.get("baths")
            instant_book = form.cleaned_data.get("instant_book")
            superhost = form.cleaned_data.get("superhost")
            amenities = form.cleaned_data.get("amenities")
            facilities = form.cleaned_data.get("facilities")

            filter_args = {}

            if city != "Anywhere":
                filter_args["city__startswith"] = city

            filter_args["country"] = country

            if room_type is not None:
                filter_args["room_type"] = room_type

            if price is not None:
                filter_args["price__lte"] = price

            if guests is not None:
                filter_args["guests__gte"] = guests

            if bedrooms is not None:
                filter_args["bedrooms__gte"] = bedrooms

            if beds is not None:
                filter_args["beds__gte"] = beds

            if baths is not None:
                filter_args["baths__gte"] = baths

            if instant_book is True:
                filter_args["instant_book"] = True

            if superhost is True:
                filter_args["host__superhost"] = True

            if len(amenities) > 0:
                filter_args["amenities"] = amenity

            if len(facilities) > 0:
                filter_args["facilities"] = facility

            qs = models.Room.objects.filter(**filter_args).order_by("-created")
            paginator = Paginator(qs, 1)
            page = request.GET.get("page", 1)
            rooms = paginator.get_page(page)
            query_string = request.GET.urlencode()
            query_string_list = query_string.split("&")
            new_query_string = ""

            for query_string_item in query_string_list:
                if "page" not in query_string_item:
                    new_query_string += query_string_item + "&"

            print(new_query_string)
            return render(
                request,
                "rooms/search.html",
                {"form": form, "rooms": rooms, "query_string": new_query_string},
            )
    else:
        # country key에 대한 value = None이면 default form을 보여준다.
        form = forms.SearchForm()

    return render(request, "rooms/search.html", {"form": form})


class EditRoomView(user_mixins.LoggedOnlyView, UpdateView):
    model = models.Room
    template_name = "rooms/room_edit.html"
    fields = (
        "name",
        "description",
        "country",
        "city",
        "price",
        "address",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "host",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
    )

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        print(self)
        if room.host.pk != self.request.user.pk:
            raise Http404
        return room


class RoomPhotosView(user_mixins.LoggedOnlyView, DetailView):
    model = models.Room
    template_name = "rooms/room_photos.html"

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404
        return room


@login_required
def delete_photo(request, room_pk, photo_pk):
    user = request.user
    try:
        room = models.Room.objects.get(pk=room_pk)
        if room.host.pk != user.pk:
            messages.error(request, "Can't delete that photo")
        else:
            # 여기서 get으로 쓰는 것과 filter을 쓰는 것의 차이는 뭘까
            # models.Photo.objects.get(pk=photo_pk).delete()
            models.Photo.objects.filter(pk=photo_pk).delete()
            messages.error(request, "Photo deleted")
        return redirect(reverse("rooms:photos", kwargs={"pk": room_pk}))
    except models.Room.DoesNotExist:
        return redirect(reverse("core:home"))


class AddPhotoView(user_mixins.LoggedOnlyView, SuccessMessageMixin, FormView):
    model = models.Photo
    template_name = "rooms/photo_add.html"
    form_class = forms.CreatePhotoForm
    fields = (
        "caption",
        "file",
    )

    def form_valid(self, form):
        pk = self.kwargs.get('pk')
        form.save(pk)
        messages.success(self.request, "Photo uploaded")
        return redirect(reverse("rooms:photos", kwargs={"pk":pk}))