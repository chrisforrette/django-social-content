from django.contrib import admin

from .forms import SocialAccountAdminForm
from .models import SocialAccount, SocialPost


class SocialAccountAdmin(admin.ModelAdmin):
    model = SocialAccount
    form = SocialAccountAdminForm
    list_display = (
        'social_content_type',
        'identifier',
        'order',
        'has_import_error',
        'created',
        'status',
    )

    list_filter = (
        'status',
        'has_import_error',
        'social_content_type',
    )

    list_editable = (
        'order',
        'has_import_error',
        'status',
    )


class SocialPostAdmin(admin.ModelAdmin):
    model = SocialPost
    list_display = (
        'body',
        'social_content_type',
        'created',
        'status',
        'linked_image',
        'linked_url',
        'social',
    )

    list_filter = (
        'social',
        'social_content_type',
    )

    exclude = ('payload',)

    readonly_fields = (
        'body',
        'social_content_type',
        'created',
        'image',
        'url',
        'social',
        'post_id',
    )

    def linked_image(self, obj):
        return '<a href="%s" target="_blank">%s</a>' % (obj.image, obj.image) if obj.image else ''

    linked_image.short_description = 'Image'
    linked_image.allow_tags = True

    def linked_url(self, obj):
        return '<a href="%s" target="_blank">%s</a>' % (obj.url, obj.url) if obj.url else ''

    linked_url.short_description = 'URL'
    linked_url.allow_tags = True
