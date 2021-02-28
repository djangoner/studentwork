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

class OrderWorkForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    subject     = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'Например: Биология'}),
                        label="Предмет")
    theme       = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'Например: анатомия человека'}),
                        label="Тема работы")
    type        = forms.ChoiceField(choices=models.DOCUMENT_TYPES, required=True,
                        label="Тип работы")
    pages_count = forms.IntegerField(max_value=100, min_value=1, required=True,
                        label="Количество страниц")
    deadline    = forms.DateField(required=True,
                        label="Срок")
    email       = forms.EmailField(required=True, max_length=60, widget=forms.TextInput(attrs={'placeholder': 'user@gmail.com'}),
                        label="Ваш e-mail")
    comment     = forms.CharField(max_length=500, widget=forms.Textarea(attrs={"rows":2, 'placeholder': 'Комментарий...'}), required=False,
                        label="Комментарий к работе")
