import django
from django.conf import settings
from django.db import models
import inspect

# ---------- settings ----------
settings.configure(
    DEBUG=True,
    ROOT_URLCONF=__name__,
    INSTALLED_APPS=[
        '__main__',
    ]
)

django.setup()

# ---------- urls ----------
from django.conf.urls import url
from django.http import HttpResponse

def dummy_view(request, id):
    return HttpResponse("ok")

urlpatterns = [
    url(r'^mymodel/(?P<id>\d+)/$', dummy_view, name='mymodel_detail'),
]

# ---------- model ----------
class MyModel(models.Model):
    name = models.CharField(max_length=100)

    def get_absolute_url(self):
        return (
            'mymodel_detail',
            (self.id,),
        )

# ---------- main ----------
def main():
    instance = MyModel(id=1)

    from django.db.models import permalink
    url = permalink(instance.get_absolute_url)()
    print("get_absolute_url result:", url)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(permalink))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
