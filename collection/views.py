from django.http import HttpResponseRedirect
from django.shortcuts import render

from collection.models import Collection
import collection.forms


def collection_list(request):
    context = {}

    context['collections'] = Collection.objects.filter(owner=request.user)

    return render(request, 'collection/list.html', context=context)


def create_global_sets_collection(request):
    context = {}

    context['form'] = collection.forms.GlobalSetsCollectionForm()

    return render(request, 'collection/create_global_sets_collection.html', context=context)


def create_global_cards_collection(request):
    context = {}

    if request.method == 'POST':
        form = collection.forms.GlobalCardsCollectionForm(request.POST, user=request.user)

        if form.is_valid():
            collection_obj = form.save(commit=False)

            collection_obj.save()
            form.save_m2m()

            collection_obj.generate_cards_collection()

            return HttpResponseRedirect('/collections')
        else:
            context['errors'] = form.errors


    context['form'] = collection.forms.GlobalCardsCollectionForm()

    return render(request, 'collection/create_global_cards_collection.html', context=context)


def create_sets_collection(request):
    context = {}

    context['form'] = collection.forms.SpecificSetsCollectionForm()

    return render(request, 'collection/create_sets_collection.html', context=context)


def create_cards_collection(request):
    context = {}

    context['form'] = collection.forms.SpecificCardsCollectionForm()

    return render(request, 'collection/create_cards_collection.html', context=context)


def collection_detail(request, id):
    context = {}

    context['collection'] = Collection.objects.get(id=id)

    return render(request, 'collection/detail.html', context=context)
