from .models import ManageDevice
'''
import django_filters


class DeviceFilter(django_filters.FilterSet):
	brand = django_filters.CharFilter(lookup_expr="icontains")
	model = django_filters.CharFilter(lookup_expr="icontains")
	kind = django_filters.CharFilter(lookup_expr="icontains")
	provider = django_filters.CharFilter(lookup_expr="icontains")

	class Meta:
		model = ManageDevice
		fields = ["brand","model","kind","provider"]
'''