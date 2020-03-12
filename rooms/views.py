from django_countries import countries
from django.views.generic import ListView, DetailView
from django.shortcuts import render
from . import models

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
    paginate_by = 10
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
    city = request.GET.get("city", "Anywhere")
    city = str.capitalize(city)
    country = request.GET.get("country", "KR")
    room_type = int(request.GET.get("room_type", 0))
    price = int(request.GET.get("price", 0))
    guests = int(request.GET.get("guests", 0))
    bedrooms = int(request.GET.get("bedrooms", 0))
    beds = int(request.GET.get("beds", 0))
    baths = int(request.GET.get("baths", 0))
    instant = request.GET.get("instant", False)
    super_host = request.GET.get("super_host", False)
    s_amenities = request.GET.getlist("amenities")
    s_facilities = request.GET.getlist("facilities")

    form = {
        "city": city,
        "s_room_type": room_type,
        "s_country": country,
        "price": price,
        "guests": guests,
        "bedrooms": bedrooms,
        "beds": beds,
        "baths": baths,
        "s_amenities": s_amenities,
        "s_facilities": s_facilities,
        "instant": instant,
        "super_host": super_host,
    }

    room_types = models.RoomType.objects.all()
    amenities = models.Amenity.objects.all()
    facilities = models.Facility.objects.all()

    choices = {
        "countries": countries,
        "room_types": room_types,
        "amenities": amenities,
        "facilities": facilities,
    }

    filter_args = {}

    if city != "Anywhere":
        filter_args["city__startswith"] = city

    filter_args["country"] = country

    if room_type != 0:
        filter_args["room_type__pk__exact"] = room_type

    rooms = models.Room.objects.filter(**filter_args)

    print(rooms)
    return render(request, "rooms/search.html", {**form, **choices, "rooms": rooms})

