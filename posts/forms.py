from django import forms
from django.forms import modelformset_factory
from .models import Post, Image, Tag


class PostForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        help_text="Enter tags separated by commas.")

    class Meta:
        model = Post
        fields = ['title', 'content']

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            # Retrieve and set initial tags as a comma-separated list
            self.initial['tags'] = ", ".join(
                tag.name for tag in self.instance.tags.all())

    def save(self, commit=True):
        instance = super(PostForm, self).save(commit=False)
        if commit:
            instance.save()
            self.save_tags(instance)
        return instance

    def save_tags(self, instance):
        tags_str = self.cleaned_data['tags']
        # Parse tags: strip whitespace, convert to lowercase, and split by
        # commas
        tags_names = [tag.strip().lower()
                      for tag in tags_str.split(',') if tag.strip()]
        # Create or fetch tags, and associate them with the post
        tags = [Tag.objects.get_or_create(name=tag)[0] for tag in tags_names]
        instance.tags.set(tags)


class ImageForm(forms.ModelForm):
    image_file = forms.ImageField(label='Image', required=True)

    class Meta:
        model = Image
        fields = ['image_file']


ImageFormSet = modelformset_factory(
    Image,
    form=ImageForm,
    extra=10,    # Number of extra forms to display
    max_num=10,  # Allow up to 10 images per post
    can_delete=True  # Allow deleting forms
)


class PostForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        help_text="Enter tags separated by commas.")

    class Meta:
        model = Post
        fields = ['title', 'content']

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            # Retrieve and set initial tags as a comma-separated list
            self.initial['tags'] = ", ".join(
                tag.name for tag in self.instance.tags.all())

    def save(self, commit=True):
        instance = super(PostForm, self).save(commit=False)
        if commit:
            instance.save()
            self.save_tags(instance)
        return instance

    def save_tags(self, instance):
        tags_str = self.cleaned_data['tags']
        # Parse tags: strip whitespace, convert to lowercase, and split by
        # commas
        tags_names = [tag.strip().lower()
                      for tag in tags_str.split(',') if tag.strip()]
        # Create or fetch tags, and associate them with the post
        tags = [Tag.objects.get_or_create(name=tag)[0] for tag in tags_names]
        instance.tags.set(tags)


class ImageForm(forms.ModelForm):
    image_file = forms.ImageField(label='Image', required=True)

    class Meta:
        model = Image
        fields = ['image_file']


ImageFormSet = modelformset_factory(
    Image,
    form=ImageForm,
    extra=10,    # Number of extra forms to display
    max_num=10,  # Allow up to 10 images per post
    can_delete=True  # Allow deleting forms
)
