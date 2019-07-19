from django.views import generic
from foodreview.models import Restaurant, Review, Like, Region
import datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, CreateView , DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import *


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_rests = Restaurant.objects.all().count()
    num_regions = Region.objects.all().count()
    num_reviews = Review.objects.all().count()
    num_likes = Like.objects.all().count()

    context = {
        'num_rests': num_rests,
        'num_regions': num_regions,
        'num_reviews': num_reviews,
        'num_likes': num_regions,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

class RestListView(ListView):
    model = Restaurant
    template_name = 'foodreview/rest_list.html'
    context_object_name = 'rest_list'

class RestDetailView(DetailView):
    model = Restaurant
    template_name = 'foodreview/rest_detail.html'
    context_object_name = 'rest'

class RegionListView(ListView):
    model = Region
    template_name = 'foodreview/region_list.html'
    context_object_name = 'region_list'

    def get_queryset(self):
        return Region.objects.order_by('name')  # Get Region Name sorted by Alphabet

class RegionDetailView(DetailView):
    model = Region
    template_name = 'foodreview/region_detail.html'


class ReviewCreate(CreateView):
    model = Review
    fields = (
        'restid','comment', 'dateofvisit','price', 'overallRating','user','likes')
    template_name = 'foodreview/review_form.html'
    labels = {
        'restid': 'restaurant name',}


class ReviewsByUser(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = Review
    template_name = 'foodreview/review_list_user.html'
    paginate_by = 10

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user).order_by('id')

class ReviewsByAll(PermissionRequiredMixin, generic.ListView):
    """Generic class-based view listing all books on loan. Only visible to users with can_mark_returned permission."""
    model = Review
    permission_required = 'foodreview.all_review'
    template_name = 'foodreview/review_list_all.html'
    paginate_by = 10

    def get_queryset(self):
        return Review.objects.order_by('id')

def post_detail(request, id):
    post = get_object_or_404(Review, id=id)
    reviews = Review.objects.filter(id=id).order_by('-id')

    context = {
        'post': post,
        'reviews': reviews,
    }

    return render(request, 'foodreview/post_detail', context)