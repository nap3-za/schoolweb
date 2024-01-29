from django.contrib import admin
from .models import TeacherAccount

# Register your models here.
class TeacherAccountAdmin(admin.ModelAdmin):
	list_display = ('user', 'sub1')
	readonly_fields = ()
	search_fields = ('user',)

	fieldsets = ()
	list_filter = ()
	filter_horizontal = ()

	class Meta:
		model = TeacherAccount

admin.site.register(TeacherAccount, TeacherAccountAdmin)