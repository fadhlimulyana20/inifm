from django import forms
from .models import Post
from froala_editor.widgets import FroalaEditor

class PostForm(forms.ModelForm):
    content = forms.CharField(widget=FroalaEditor(options={
        'toolbarInline': False,
        'heightMin': 300,
    }))
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Type some Title'}))

    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'status',
            'category',
            'featured_image'
        ]

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'