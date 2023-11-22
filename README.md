# django-rest-POC

### Description of project
- This project is created for purpose for using django Rest Framework API views like APIView, GenericAPIView, ModelViewSet, mixins and other related libraries
- There is also ORM querying methods used for creating APIs 

Django provides a variety of methods and classes for querying the database using its Object-Relational Mapping (ORM) system. Here are some commonly used methods and classes for querying in Django models:
1. Filtering:

* `filter(**kwargs)`: Returns a QuerySet that matches the given lookup parameters.
* `exclude(**kwargs)`: Returns a QuerySet that does not match the given lookup parameters.

2. Q objects:
* `Q()`: Allows complex queries using | (OR), & (AND), and ~ (NOT) operators.
```
from django.db.models import Q
queryset = MyModel.objects.filter(Q(field1=value1) | Q(field2=value2))
```
3. F objects:
* `F()`: Represents a database column or value in a query. Allows referencing the value of a database field within a query.
```
from django.db.models import F
queryset = MyModel.objects.filter(field1__gt=F('field2'))
```
```
from django.db.models import F

MyModel.objects.filter(id=1).update(counter=F('counter') + 1)

```

```
# Using F expression for referencing fields in an update.
from django.db.models import F

MyModel.objects.filter(id=1).update(counter=F('counter') + 1)
```
4. Subquery:
* `Subquery()`: Represents a subquery in a queryset.
```
from django.db.models import Subquery
queryset = MyModel.objects.filter(field1__in=Subquery(OtherModel.objects.values('field2')))
```
5. Exists:
* `exists()`: Returns True if the queryset contains any results, False otherwise.
```
queryset = MyModel.objects.filter(field1=value1)
if queryset.exists():
    # Do something
```

6. OuterRef and Subquery:
* `OuterRef` and `Subquery` are used for nested queries.
```
from django.db.models import OuterRef, Subquery

subquery = Subquery(OtherModel.objects.filter(id=OuterRef('id')).values('field'))
queryset = MyModel.objects.annotate(other_model_field=subquery)
```

7. Exists and OuterRef:
* Using `Exists` with `OuterRef` for correlated subqueries.
```
from django.db.models import Exists

subquery = OtherModel.objects.filter(parent_id=OuterRef('id'))
queryset = MyModel.objects.annotate(has_children=Exists(subquery))
```

8. `Avg`, `Sum`, `Min`, `Max`:
* Aggregation functions for average, sum, min, and max.
```
from django.db.models import Avg, Sum, Min, Max

avg_value = MyModel.objects.aggregate(avg_field=Avg('numeric_field'))
sum_value = MyModel.objects.aggregate(sum_field=Sum('numeric_field'))
min_value = MyModel.objects.aggregate(min_field=Min('numeric_field'))
max_value = MyModel.objects.aggregate(max_field=Max('numeric_field'))
```

9. Count :
* `count()`: Returns the number of objects in the queryset.
```
count = MyModel.objects.filter(field1=value1).count()
```

10. Count with Group By:
* Using `values()` and `annotate()` for counting with grouping.
```
from django.db.models import Count

queryset = MyModel.objects.values('category').annotate(category_count=Count('id'))
```

11. Distinct:
* `distinct()`: Returns a queryset with duplicate rows removed.
```
distinct_queryset = MyModel.objects.values('field1').distinct()
```

12. Aggregate:
* `aggregate()`: Performs an aggregate operation on the queryset.
```
from django.db.models import Avg
avg_value = MyModel.objects.aggregate(avg_field=Avg('field1'))
```
13. Annotate:
* `annotate()`: Adds annotations to each object in the queryset.
```
from django.db.models import Count
annotated_queryset = MyModel.objects.annotate(num_related=Count('related_model'))
```

14. Values and ValuesList:
* `values()`: Returns a ValuesQuerySet representing the queryset data as dictionaries.
* `values_list()`: Returns a ValuesListQuerySet representing the queryset data as tuples.

15. Raw SQL Queries:
* `raw()`: Allows execution of raw SQL queries.
```
raw_queryset = MyModel.objects.raw('SELECT * FROM myapp_mymodel')
```

16. Chaining Queries:
* You can chain multiple query methods to refine your queryset.
```
queryset = MyModel.objects.filter(field1=value1).exclude(field2=value2).order_by('-date_field')
```
17. Date Queries:
* `__year`, `__month`, `__day`, `__week_day`, etc.
```
queryset = MyModel.objects.filter(date_field__year=2023, date_field__month=11)
```
* Filtering records within a date range.
```
from django.utils import timezone

start_date = timezone.now() - timezone.timedelta(days=7)
end_date = timezone.now()
queryset = MyModel.objects.filter(date_field__range=(start_date, end_date))
```
18. Range Queries:
* `__range`
```
queryset = MyModel.objects.filter(date_field__range=(start_date, end_date))
```

19. Filtering by Date Range:
* Filtering records within a date range.
```
from django.utils import timezone

start_date = timezone.now() - timezone.timedelta(days=7)
end_date = timezone.now()
queryset = MyModel.objects.filter(date_field__range=(start_date, end_date))
```

20. Case When:
* `Case`, `When`, `F`
```
from django.db.models import Case, When, Value
queryset = MyModel.objects.annotate(status=Case(
    When(field1=value1, then=Value('Active')),
    default=Value('Inactive'),
    output_field=CharField(),
))
```
```
from django.db.models import Case, When, Value, Sum

queryset = MyModel.objects.annotate(
    total=Sum(Case(When(condition=True, then=Value(1)), default=Value(0))),
)
```
21. Aggregate with Group By:
* Grouping using `values()` and aggregating using `annotate()`
```
from django.db.models import Count
queryset = MyModel.objects.values('category').annotate(category_count=Count('id'))
```

22. Prefetch Related:
* `prefetch_related()`: Fetches related objects for a queryset to minimize database queries.
```
queryset = MyModel.objects.prefetch_related('related_model')
```

23. Window Functions:
* `Window`, `F`, `ExpressionWrapper`
```
from django.db.models import Window, F, ExpressionWrapper, fields
queryset = MyModel.objects.annotate(
    row_number=Window(
        expression=RowNumber(),
        order_by=F('date_field').desc(),
    ),
    difference=ExpressionWrapper(
        F('field1') - F('field2'),
        output_field=fields.FloatField(),
    ),
)
```
24. Window Functions with Partition By:
* Using `Window` with partitioning.
```
from django.db.models import Window, F

queryset = MyModel.objects.annotate(
    row_number=Window(
        expression=RowNumber(),
        partition_by=[F('category')],
        order_by=F('date_field').desc(),
    ),
)
```

25. Bulk Update:
* `update()`: Updates multiple records in a single query.
```
MyModel.objects.filter(field1=value1).update(field2=new_value)
```

26. Raw SQL Queries with Parameters:
* Using parameters with raw SQL queries.
```
queryset = MyModel.objects.raw('SELECT * FROM myapp_mymodel WHERE field1=%s', [value1])
```

27. Combining OR Conditions:
* Using `Q` objects to combine multiple OR conditions.

```
queryset = MyModel.objects.filter(Q(field1=value1) | Q(field2=value2))
```

28. Select Related:
* `select_related()`: Follows foreign key relationships and includes related objects in the queryset.
```
queryset = MyModel.objects.select_related('related_model')
```

29. Custom Manager Methods:
* Adding custom methods to your model's manager.
```
class MyModelManager(models.Manager):
    def custom_query(self, param):
        return self.filter(field1=param)

class MyModel(models.Model):
    objects = MyModelManager()
```


30. Custom Aggregation with Func:
* Using `Func` for custom aggregation functions.
```
from django.db.models import Func, F

class CustomAvg(Func):
    function = 'AVG'
    template = '%(function)s(%(distinct)s%(expressions)s)'

queryset = MyModel.objects.annotate(avg_custom=CustomAvg(F('numeric_field')))
```





































































