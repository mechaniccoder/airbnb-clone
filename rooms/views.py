from django.utils import timezone
from django.views.generic import ListView
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        context["now"] = now
        return context
