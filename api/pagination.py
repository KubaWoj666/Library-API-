from rest_framework.pagination import PageNumberPagination


class ReviewPagination(PageNumberPagination):
    page_size = 5
    page_query_param = "page"
    page_size_query_param = "page_size"