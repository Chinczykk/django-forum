from django.contrib import admin
from .models import Section, Topic, Comment

# Register your models here.

class SectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'description', 'created')
    list_filter = ('owner', 'created')
    search_fields = ('name', 'owner')
    raw_id_fields = ('owner',)
    date_hierarchy = 'created'
    ordering = ['created']

admin.site.register(Section, SectionAdmin)

class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'body', 'created', 'updated', 'section')
    list_filter = ('owner', 'created')
    search_fields = ('name', 'owner')
    raw_id_fields = ('owner',)
    date_hierarchy = 'created'
    ordering = ['created', 'section']

admin.site.register(Topic, TopicAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('owner', 'body', 'created', 'topic')
    list_filter = ('owner', 'created')
    search_fields = ('owner',)
    raw_id_fields = ('owner',)
    date_hierarchy = 'created'
    ordering = ['created', 'topic']

admin.site.register(Comment, CommentAdmin)