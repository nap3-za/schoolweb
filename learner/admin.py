from django.contrib import admin
from .models import LearnerAccount

# Register your models here.
class LearnerAccountAdmin(admin.ModelAdmin):

	list_display = ('user', 'grade', 'stream')
	readonly_fields = ()
	search_fields = ('user', 'stream', 'grade', 'club', 'sport')

	fieldsets = ()
	list_filter = ()
	filter_horizontal = ()

	class Meta:
		model = LearnerAccount

admin.site.register(LearnerAccount, LearnerAccountAdmin)