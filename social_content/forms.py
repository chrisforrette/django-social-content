from django import forms

from .models import SocialAccount


class SocialAccountAdminForm(forms.ModelForm):
    class Meta:
        model = SocialAccount
        exclude = ()
        widgets = {
            'raw_identifier': forms.HiddenInput()
        }
        labels = {
            'raw_identifier': ''
        }

    def clean(self):
        data = super(SocialAccountAdminForm, self).clean()
        identifier = data.get('identifier')

        if identifier and data['social_content_type'] in ['instagram', 'facebook']:
            try:
                raw_id = getattr(SocialAccount, 'fetch_%s_raw_id' % data['social_content_type'])(identifier)
                if raw_id:
                    data['raw_identifier'] = raw_id
                else:
                    raise forms.ValidationError('Invalid %s username entered, please check your input and try again' % data['social_content_type'].title(), code='invalid')
            except Exception, e:
                raise forms.ValidationError('%s generated an error with the identifier you entered: %s' % (data['social_content_type'].title(), str(e)), code='invalid')

        return data
