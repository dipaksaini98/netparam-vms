import django_filters
from .models import Visit, Employee, Visitor
from django_filters import DateFilter


class VisitFilter(django_filters.FilterSet):
    # start_date = DateFilter(field_name="date_visited", lookup_expr='gte')
    # end_date = DateFilter(field_name="date_visited", lookup_expr='lte')

    class Meta:
        model = Visit
        fields = '__all__'
        exclude = ['employee', 'date_visited']
