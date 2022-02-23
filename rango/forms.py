from django import forms
from rango.models import Page, Category

# each model has one form class


class CategoryForm(forms.ModelForm):
    # 4 attributes and form settings
    # HiddenInput(): hide one attributes (not display)
    name = forms.CharField(max_length=Category.NAME_MAX_LENGTH,
                           help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # adding additional info here
    class Meta:
        model = Category
        fields = ('name',)


class PageForm(forms.ModelForm):
    # 4 attributes and form settings
    title = forms.CharField(max_length=Page.TITLE_MAX_LENGTH,
                            help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=Page.URL_MAX_LENGTH,
                         help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    # adding addtional info here
    class Meta:
        model = Page

        # exclude category field, another method: field('title', 'url', 'views')
        exclude = ('category',)

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        # once url is not null and dosen't start with 'http://', prepend it
        if url and not url.startswith('http://'):
            url = f'http://{url}'
            cleaned_data['url'] = url

        return cleaned_data
