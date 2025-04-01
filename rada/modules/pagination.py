from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 15

class CustomItemPagination(PageNumberPagination):
    
    page_size_query_param = 'page_size'
    
    def get_page_size(self, request):
        if request.query_params.get("pagesize", None) is not None:
            try:
                pageSize = int(request.query_params.get("pagesize"))
                return pageSize
            except TypeError:
                pass
        return super().get_page_size(request)