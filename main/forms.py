from django import forms
from . import models


class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = models.Document
        fields = [
            'file', 'title', 'annotation', 'type', 'discipline', 'created_year', 'language',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True
