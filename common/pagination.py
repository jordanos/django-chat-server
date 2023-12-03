from rest_framework import pagination
from rest_framework.response import Response


class CustomPagination(pagination.PageNumberPagination):
    page_size_query_param = "page_size"

    def get_paginated_response(self, data):
        return Response(
            {
                "page_metadata": {
                    "total_pages": self.page.paginator.num_pages,
                    "count": self.page.paginator.count,
                    "page_size": self.get_page_size(self.request),
                },
                "results": data,
            }
        )

    def get_paginated_response_schema(self, schema):
        return {
            "type": "object",
            "properties": {
                "page_metadata": {
                    "type": "object",
                    "properties": {
                        "total_pages": {"type": "integer", "example": 1},
                        "count": {"type": "integer", "example": 10},
                        "page_size": {"type": "integer", "example": 5},
                    },
                },
                "results": schema,
            },
        }
