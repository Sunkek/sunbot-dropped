from django.db import connection
from django.db.utils import IntegrityError
from django.db.models import Sum
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import viewsets, pagination
from rest_framework.response import Response

from api.serializers import NwordsSerializer, NwordsTopSerializer
from api.pagination import CustomPageNumberPagination
from api.models import User, Guild, Nwords

from utils import activity_functions, helpers


class NwordsViewSet(viewsets.ModelViewSet):
    queryset = Nwords.objects.all()
    serializer_class = NwordsSerializer

    def partial_update(self, request, *args, **kwargs):
        """PATCH requests fall here.
        Here I'm working from the idea that the entry already exists,
        so I just find it and update the counters. Only if it doesn't exist,
        I create a new one and try to save it. If it can't save because
        there's no member in the database, I create that member."""
        try:
            data = request.data
            try:
                # Find the existing message entry
                nwords = Nwords.objects.get(
                    guild_id=Guild(guild_id=data["guild_id"]),
                    user_id=User(user_id=data["user_id"]),
                    period=data["period"]
                )
            except ObjectDoesNotExist:
                # Entry not found - create one!
                nwords = Nwords(
                    guild_id=Guild(guild_id=data["guild_id"]),
                    user_id=User(user_id=data["user_id"]),
                    period=data["period"]
                )
            # Update counters
            nwords.nigger += data["nigger"]
            nwords.nigga += data["nigga"]
            try:
                # Submit changes
                nwords.save()
            except IntegrityError:
                # If there's no member - create one!
                user = User(user_id=data["user_id"])
                user.save()
                nwords.save()
            serializer = self.get_serializer(nwords)
            return Response(serializer.data)
        except Exception as e:
            print(e)


class TopNwordsViewSet(viewsets.ModelViewSet):
    queryset = Nwords.objects.all()
    serializer_class = NwordsSerializer
    pagination_class = CustomPageNumberPagination
    
    def get_paginated_response(self, data, total_nigger, total_nigga):
        """
        Return a paginated style `Response` object for the given output data.
        I just want to add total to my results.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(
            data, total_1=total_nigger, total_2=total_nigga,
        )

    def list(self, request, time_range, *args, **kwargs):
        try:
            data = request.data
            
            cursor = connection.cursor()
            cursor.execute(f"""
                SELECT 
                    user_id,
                    sum(nigger) as nigger_count,
                    sum(nigga) as nigga_count,
                    sum(nigger) + sum(nigga) as total_count
                FROM nwords
                WHERE guild_id = %s
                GROUP BY user_id
                ORDER BY total_count DESC""",
                [data['guild_id'], ]
            )
            total_nigger = Nwords.objects.aggregate(total=Sum("nigger"))["total"]
            total_nigga = Nwords.objects.aggregate(total=Sum("nigga"))["total"]
            result = helpers.dictfetchall(cursor)
            page = self.paginate_queryset(result)
            if page is not None:
                serializer = NwordsTopSerializer(page, many=True)
                return self.get_paginated_response(serializer.data, total_nigger, total_nigga)
            serializer = NwordsTopSerializer(result, many=True)
            cursor.close()
            return Response(serializer.data)
        except Exception as e:
            print(e)


"""Define the allowed request methods for each ModelViewSet"""
nwords = NwordsViewSet.as_view({
    'patch': 'partial_update',
})
top_nwords = TopNwordsViewSet.as_view({
    'get': 'list',
})