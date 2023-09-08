from django.shortcuts import render, get_object_or_404, redirect, reverse
from .forms import GameReviewForm
from .models import GameReview, Publisher, Game
from django.views import generic
from django.contrib.auth.models import User  
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.views.generic.edit import FormMixin


from django.db.models import Max, F

def index(request):
    
    max_rating = GameReview.objects.aggregate(max_rating=Max('rating'))['max_rating']
    latest_best_review = GameReview.objects.filter(rating=max_rating).order_by('-date_created').first()
    game = None
    if latest_best_review:
        game = latest_best_review.game

    return render(request, "index.html", {'game': game, 'review': latest_best_review})


from django.contrib.auth.forms import UserCreationForm

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('index')  
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})



class PublisherView(generic.ListView):
    model = Publisher
    template_name = 'publishers.html'
    paginate_by = 3


def publisher(request, publisher_id):
    single_publisher = get_object_or_404(Publisher, pk=publisher_id)
    return render(request, 'publisher.html', {'publisher': single_publisher})


class GameListView(generic.ListView):
    model = Game
    template_name = 'games.html'
    paginate_by = 3


class GameDetailView(FormMixin, generic.DetailView):
    model = Game
    template_name = 'game.html'
    form_class = GameReviewForm

    def get_success_url(self):
        return reverse('game', kwargs={'pk': self.object.id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.game = self.object
        form.instance.reviewer = self.request.user
        form.save()
        return super(GameDetailView, self).form_valid(form)




