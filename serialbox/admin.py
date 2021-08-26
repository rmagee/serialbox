from serialbox import models
from django.contrib import admin
from list_based_flavorpack.models import ListBasedRegion
from random_flavorpack.models import RandomizedRegion
from django.utils.safestring import mark_safe

class ResponseRuleAdmin(admin.ModelAdmin):
    list_display = ('pool', 'rule', 'content_type')
    search_fields = ('pool__readable_name','pool__machine_name')

@admin.register(models.Response)
class ResponseAdmin(admin.ModelAdmin):
    def task(self):
        if self.task_name != '' and self.task_name is not None:
            return mark_safe('<a style="color: black" class="download-task" href="%(url)s%(task_name)s">%(task_name)s</a>' %
                             {'url': '/qu4rtetadmin/quartet_capture/task/?q=', 'task_name': self.task_name})
        else:
            return ''

    list_display = ('pool', 'type',
                    'size_granted', 'remote_host', task)
    search_fields = ('response',)

    def get_readonly_fields(self, request, obj=None):
        return list(self.readonly_fields) + \
               [field.name for field in obj._meta.fields] + \
               [field.name for field in obj._meta.many_to_many]



class RegionInline(admin.StackedInline):
    model = models.SequentialRegion
    extra = 0


class ListBasedInline(admin.StackedInline):
    model = ListBasedRegion
    extra = 0


class RandomRegionInline(admin.StackedInline):
    model = RandomizedRegion
    extra = 0


class PoolAdmin(admin.ModelAdmin):
    list_display = (
        'readable_name',
        'machine_name',
        'active'
    )
    search_fields = ['readable_name', 'machine_name']
    inlines = [RegionInline, ListBasedInline, RandomRegionInline]

def register_to_site(admin_site):
    admin_site.register(models.Pool, PoolAdmin)
    admin_site.register(models.ResponseRule, ResponseRuleAdmin)
    admin_site.register(models.Response, ResponseAdmin)

