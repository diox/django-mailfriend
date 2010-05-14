from django import forms

from mailfriend.models import MailedItem

class MailedItemForm(forms.ModelForm):

    user_email_as_from = forms.BooleanField(label="Use my e-mail address as from address", required=False)
    send_to_user_also = forms.BooleanField(label="Send myself a copy of this e-mail", required=False)
    
    def clean(self):
        dst = self.cleaned_data['mailed_to']
        src = self.instance.mailed_by
        content_type = self.instance.content_type
        object_pk = self.instance.object_pk        
        
        if MailedItem.objects.filter(mailed_by=src, mailed_to=dst, object_pk=object_pk, content_type=content_type).count():
            raise forms.ValidationError("You already sent a mail to this address about the same content!")

        return self.cleaned_data

    class Meta:
        model = MailedItem
        exclude = ('mailed_by', 'date_mailed', 'content_type', 'object_pk')
