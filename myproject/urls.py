from django.urls import path, include
from django.http import JsonResponse
from django.views.generic import TemplateView

def root(request):
    return JsonResponse({
        "message": "Blog API is running!",
        "endpoints": {
            "list_create": "/api/blogs/",
            "detail": "/api/blogs/<id>/",
        }
    })

urlpatterns = [
    path('', TemplateView.as_view(template_name='blog_ui.html'), name='ui'),
    path('api/', include('myapp.urls')),
]