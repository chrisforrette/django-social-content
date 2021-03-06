from django.conf import settings


DEFAULTS = {
    'SOCIAL_CONTENT_TYPES': (
        'Facebook',
        'Twitter',
        'Instagram',
    ),

    'SOCIAL_CONTENT_MAX_POSTS': None,

    # Facebook

    'FACEBOOK_APP_ID': None,
    'FACEBOOK_APP_SECRET': None,

    # Twitter

    'TWITTER_CONSUMER_KEY': None,
    'TWITTER_CONSUMER_SECRET': None,
    'TWITTER_ACCESS_TOKEN_KEY': None,
    'TWITTER_ACCESS_TOKEN_SECRET': None,

    # Instagram

    'INSTAGRAM_CLIENT_ID': None,
    'INSTAGRAM_CLIENT_SECRET': None,
    'INSTAGRAM_ACCESS_TOKEN': None,

    # YouTube

    'YOUTUBE_APP_API_KEY': None,

    # Tumblr

    'TUMBLR_API_CONSUMER_KEY': None
}


for setting in DEFAULTS.keys():
    try:
        getattr(settings, setting)
    except AttributeError:
        setattr(settings, setting, DEFAULTS[setting])
