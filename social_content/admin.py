from django.contrib import admin

from .forms import SocialAccountAdminForm
from .models import SocialAccount, SocialPost


class SocialAccountAdmin(admin.ModelAdmin):
    model = SocialAccount
    form = SocialAccountAdminForm
    list_display = (
        'identifier',
        'social_content_type',
        'created',
        'status',
        'last_import_error',
    )

    list_filter = (
        'status',
        'social_content_type',
    )

    list_editable = (
        'status',
    )

    readonly_fields = (
        'last_import_error',
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
        'social_account',
    )

    list_filter = (
        'social_account',
        'social_content_type',
    )

    exclude = ('payload',)

    readonly_fields = (
        'body',
        'social_content_type',
        'created',
        'image',
        'url',
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
