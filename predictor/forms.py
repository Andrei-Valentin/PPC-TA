from django import forms


class DocumentForm(forms.Form):
    def is_valid(*args, **kwargs):
        return True

    file = forms.FileField(help_text='Valid .mp3 file')
