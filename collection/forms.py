from django.forms import ModelForm
from collection.models import Collection


class SpecificCardsCollectionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ModelForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Collection
        exclude = ['owner', 'sets',]

    def save(self, commit=True):
        instance = super(ModelForm, self).save(commit=False)

        instance.owner = self.user

        instance.save()

        instance.generate_cards_collection()

        return instance


class SpecificSetsCollectionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ModelForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Collection
        exclude = ['owner', 'cards',]

    def save(self, commit=True):
        instance = super(ModelForm, self).save(commit=False)

        instance.owner = self.user

        instance.save()

        instance.generate_sets_collection()

        return instance


class GlobalSetsCollectionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ModelForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Collection
        exclude = ['owner', 'cards']
        exclude.extend(Collection.LANGUAGES)

    def save(self, commit=True):
        instance = super(ModelForm, self).save(commit=False)

        instance.owner = self.user

        instance.english = True
        instance.t_chinese = True
        instance.s_chinese = True
        instance.french = True
        instance.german = True
        instance.italian = True
        instance.japanese = True
        instance.korean = True
        instance.portuguese = True
        instance.russian = True
        instance.spanish = True

        instance.save()

        instance.generate_sets_collection()

        return instance


class GlobalCardsCollectionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ModelForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Collection
        exclude = ['owner', 'sets']
        exclude.extend(Collection.LANGUAGES)

    def save(self, commit=True):
        instance = ModelForm.save(self, commit=False)

        instance.owner = self.user

        instance.english = True
        instance.t_chinese = True
        instance.s_chinese = True
        instance.french = True
        instance.german = True
        instance.italian = True
        instance.japanese = True
        instance.korean = True
        instance.portuguese = True
        instance.russian = True
        instance.spanish = True

        return instance
