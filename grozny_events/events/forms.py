from django import forms

from .models import Event, Comment


class EventForm(forms.ModelForm):
    """Форма для создания/редактирования публикации."""

    class Meta:
        model = Event
        fields = (
            'title', 'category', 'image', 'date',
            'description', 'location', 'additionally',
        )


class CommentForm(forms.ModelForm):
    """Форма для написания комментария к публикации."""

    class Meta:
        model = Comment
        fields = ('text', 'rate',)
