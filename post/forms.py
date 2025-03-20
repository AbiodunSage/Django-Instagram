from django import forms
from .models import Post, PostFile  # Import PostFile

class PostForm(forms.ModelForm):
    file = forms.FileField(
        required=True,
        widget=forms.ClearableFileInput(attrs={'accept': 'image/*,video/*'})
    )
    caption = forms.CharField(max_length=150, required=False)

    class Meta:
        model = Post
        fields = ['caption']  # Only caption here!  'file' is handled separately

    def clean_file(self):
        file = self.cleaned_data.get('file')

        if not file:
            raise forms.ValidationError('You must provide an image or a video.')

        valid_extensions = ['.jpg', '.jpeg', '.png', '.mp4', '.mov', '.avi']
        if not any(file.name.lower().endswith(ext) for ext in valid_extensions):
            raise forms.ValidationError('Unsupported file type. Please upload an image or video.')

        return file