from django.core.exceptions import NON_FIELD_ERRORS
from django.core.paginator import Paginator
from django.db.models import Count
from django.forms import modelformset_factory, inlineformset_factory
from django.forms.formsets import ORDERING_FIELD_NAME
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import RedirectView
from django.views.generic.dates import ArchiveIndexView, MonthArchiveView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .forms import BbForm, RubricBaseFormSet
from .models import Bb, Rubric


def index(request):
    bbs = Bb.objects.all()
    rubrics = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)

    paginator = Paginator(bbs, 2, orphans=2)
    # paginator = Paginator(bbs, 1, orphans=0)

    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1

    page = paginator.get_page(page_num)

    context = {'rubrics': rubrics, 'page_obj': page, 'bbs': page.object_list}

    return render(request, 'index.html', context)


class BbIndexView(ListView):
    model = Bb
    template_name = 'index.html'
    context_object_name = 'bbs'
    paginate_by = 2
    paginate_orphans = 2

    def get_queryset(self):
        return Bb.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
        return context


# class BbIndexView(ArchiveIndexView):
#     model = Bb
#     template_name = 'index.html'
#     date_field = 'published'
#     date_list_period = 'month'
#     context_object_name = 'bbs'
#     allow_empty = True
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['rubrics'] = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
#         return context


class BbMonthView(MonthArchiveView):
    model = Bb
    template_name = 'index.html'
    date_field = 'published'
    date_list_period = 'month'
    month_format = '%m'
    context_object_name = 'bbs'
    allow_empty = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


class BbRedirectView(RedirectView):
    url = '/'


class BbByRubricView(ListView):
    template_name = 'by_rubric.html'
    context_object_name = 'bbs'

    def get_queryset(self):
        return Bb.objects.filter(rubric=self.kwargs['rubric_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        context['current_rubric'] = Rubric.objects.get(
            pk=self.kwargs['rubric_id'])
        return context


class BbDetailView(DetailView):
    model = Bb

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


class BbCreateView(CreateView):
    template_name = 'create.html'
    form_class = BbForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


class BbEditView(UpdateView):
    model = Bb
    form_class = BbForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubric'] = Rubric.objects.all()
        return context


class BbDeleteView(DeleteView):
    model = Bb
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubric'] = Rubric.objects.all()
        return context


def edit(request, pk):
    bb = Bb.objects.get(pk=pk)

    if request.method == 'POST':
        bbf = BbForm(request.POST, instance=bb)
        if bbf.is_valid():
            if bbf.has_changed():
                bbf.save()
            return HttpResponseRedirect(
                # reverse('bboard:by_rubric',
                #         kwargs={'rubric_id': bbf.cleaned_data['rubric'].pk})
                reverse('bboard:detail',
                        kwargs={'pk': pk})
            )
        else:
            context = {'form': bbf}
            return render(request, 'bboard/bb_form.html', context)
    else:
        bbf = BbForm(instance=bb)
        context = {'form': bbf}
        return render(request, 'bboard/bb_form.html', context)


def add_save(request):
    bbf = BbForm(request.POST)

    if bbf.is_valid():
        bbf.save()
        return HttpResponseRedirect(
            reverse('bboard:by_rubric',
                    kwargs={'rubric_id': bbf.cleaned_data['rubric'].pk})
        )
    else:
        context = {'form': bbf}
        return render(request, 'bboard/bb_form.html', context)


def rubrics(request):
    RubricFormSet = modelformset_factory(Rubric, fields=('name',), can_order=True,
                                         can_delete=True, extra=3, formset=RubricBaseFormSet)

    if request.method == 'POST':
        formset = RubricFormSet(request.POST)

        if formset.is_valid():
            instances = formset.save(commit=False)
            for obj in formset:
                if obj.cleaned_data:
                    rubric = obj.save(commit=False)
                    rubric.order = obj.cleaned_data[ORDERING_FIELD_NAME]
                    rubric.save()

            for obj in formset.deleted_objects:
                obj.delete()

            return redirect('bboard:rubrics')

    else:
        formset = RubricFormSet()

    context = {'formset': formset}

    return render(request, 'bboard/rubrics.html', context)


def bbs(request, rubric_id):
    BbsFormSet = inlineformset_factory(Rubric, Bb, form=BbForm, extra=1)
    rubric = Rubric.objects.get(pk=rubric_id)
    if request.method == 'POST':
        formset = BbsFormSet(request.POST, instance=rubric)

        if formset.is_valid():
            formset.save()
            return redirect('bboard:index')
    else:
        formset = BbsFormSet(instance=rubric)

    context = {'formset': formset, 'current_rubric': rubric}
    return render(request, 'bboard/bbs.html', context)
