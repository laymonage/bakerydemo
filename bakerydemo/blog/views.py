from django_filters.filters import DateFromToRangeFilter
from wagtail.admin.filters import DateRangePickerWidget
from wagtail.admin.ui.tables import DateColumn
from wagtail.admin.viewsets.pages import PageViewSet

from bakerydemo.blog.models import BlogPage


class BlogPageFilterSet(PageViewSet.filterset_class):
    date_published = DateFromToRangeFilter(
        label="Date published",
        widget=DateRangePickerWidget,
    )

    class Meta:
        model = BlogPage
        fields = ["slug"]


class BlogPageViewSet(PageViewSet):
    model = BlogPage
    icon = "comment"
    list_display = PageViewSet.columns + [
        "slug",
        DateColumn(
            "date_published",
            label="Date published",
            sort_key="date_published",
        ),
        "thumb_image",
    ]
    filterset_class = BlogPageFilterSet
    list_export = ["title", "latest_revision_created_at", "live", "date_published"]
    ordering = "-date_published"


class CustomPageViewSet(PageViewSet):
    list_display = PageViewSet.columns + ["slug"]
    list_filter = ["slug"]
    list_export = ["title", "slug", "latest_revision_created_at", "live"]
    ordering = "slug"
    export_filename = "pages"
