from django.contrib import admin
from .models import Post,Comments


class PostAdmin(admin.ModelAdmin):
    list_display=['title','date','upvotes','slug']
    search_fields=['title', 'content']

admin.site.register(Post,PostAdmin)
admin.site.register(Comments)