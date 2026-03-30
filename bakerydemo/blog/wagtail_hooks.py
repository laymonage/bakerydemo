from wagtail import hooks

from bakerydemo.blog.views import BlogPageViewSet, CustomPageViewSet


@hooks.register("register_admin_viewset")
def register_page_viewsets():
    return [BlogPageViewSet(), CustomPageViewSet()]
