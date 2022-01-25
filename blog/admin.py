from django.contrib import admin

from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    """ Show admin panel of the blog"""

    list_display = ('title', 'slug',
                    'status', 'created_on')
    list_filter = ("status",)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Post, PostAdmin)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """ Show admin panel for the comments"""

    list_display = ('name', 'body', 'post',
                    'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, queryset):
        """ funciton to approve comments """
        queryset.update(active=True)
