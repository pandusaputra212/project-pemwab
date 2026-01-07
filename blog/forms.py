# blog/forms.py
from django import forms
from .models import Post, Comment
from tinymce.widgets import TinyMCE


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'title',
            'category',
            'text',
            'header_image',
        )

        labels = {
            'title': 'Judul Berita',
            'category': 'Kategori Berita',
            'text': 'Isi Berita',
            'header_image': 'Gambar Header',
        }

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Masukkan judul berita',
            }),
            'category': forms.Select(attrs={
                'class': 'form-select',
            }),
            'text': TinyMCE(attrs={
                'cols': 80,
                'rows': 20,
            }),
            'header_image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text',)

        labels = {
            'author': 'Nama',
            'text': 'Komentar',
        }

        widgets = {
            'author': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
            }),
        }