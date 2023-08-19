from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, DetailView, DeleteView, TemplateView, View
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.contrib import messages
from django.urls import reverse_lazy
from rest_framework import generics
from .models import Polls      # Question, Choice
from .forms import PollsQueationForm, SharePollForm, EditPollForm     # PollsChoicesForm


# HomePage
class HomePageView(TemplateView):
    template_name = 'home.html'

# About Page
class AboutPageView(TemplateView):
    template_name = 'about.html'

# Listing Polls by User
class PollsListView(LoginRequiredMixin, ListView):
    template_name = 'polls/list_polls.html'
    paginate_by = 3 
    context_object_name = 'poll'

    def get_queryset(self):
        querryset = Polls.objects.all()
        querryset = querryset.order_by('-id')
        return querryset


# Listing User Specific Posts
class PollsByUsersView(LoginRequiredMixin, ListView):
    template_name = 'polls/my_polls_list.html'
    paginate_by = 3
    context_object_name = 'poll'

    # gets the polls tha user have created on system
    def get_queryset(self):
        querryset = Polls.objects.filter(author=self.request.user).order_by('-id')
        return querryset

    
# Creating a Poll
class PollsCreateView(CreateView):
    form_class = PollsQueationForm
    template_name = 'polls/create_polls.html'
    success_url = reverse_lazy('list_polls')

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form,})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.instance.author = self.request.user
            form.save()
            return redirect('home')
        else:
            form = PollsQueationForm()
        return render(request, self.template_name, {'form': form})


# Post Details
class PollDetailView(View):
    model = Polls
    template_name = 'polls/polls_detail.html'
    context_object_name = 'poll'

    def get(self, request, pk):
        poll = get_object_or_404(Polls, pk=pk)
        form = EditPollForm(instance=poll)
        return render(request, self.template_name, {'poll': poll, 'form': form})

    def poll(self, request, pk):
        poll = get_object_or_404(Polls, pk=pk)
        form = EditPollForm(request.POST, instance=poll)
        if form.is_valid():
            form.save()
            return redirect('poll_detail', pk=poll.pk)
        return render(request, self.template_name, {'poll': poll, 'form': form})

def share_poll(request, pk):
    # Retrieve poll by id
    poll = get_object_or_404(Polls, pk=pk,)
    sent = False

    if request.method == 'POST':
        form = SharePollForm(request.POST)
        if form.is_valid():

            # Form fields passed validation
            cd = form.cleaned_data
            # ... send the mail
            post_url = request.build_absolute_uri(poll.get_absolute_url())
            subject = f"{cd['name']} recommends you read " f"{poll.question}"
            message = f"Read {poll.question} at {post_url}\n\n" f"{cd['name']}"
            send_mail(subject, message, 'sikapa75@gmail.com', [cd['to']])
            sent = True            

            messages.success(request, 'Your Poll have been Sent')
            return redirect('poll_detail', pk=pk)
    else:
        form = SharePollForm()
    return render(request, 'polls/share_poll.html', 
                  {'poll': poll, 
                   'form': form,
                   'sent': sent,})


class EditPollView(LoginRequiredMixin, UpdateView):
    model = Polls
    form_class = EditPollForm
    template_name = 'polls/edit_poll.html'
    context_object_name = 'poll'

    def form_valid(self, form):
        edit_poll = form.save(commit=False)
        edit_poll.save()
        return redirect('poll_detail', pk=edit_poll.pk)


def vote(request, pk):
    poll = Polls.objects.get(pk=pk)
    
    if request.method == "POST":
        choice = request.POST['poll']
        if choice == 'option1':
            poll.option1_count += 1
        elif choice == 'option2':
            poll.option2_count += 1
        elif choice == 'option3':
            poll.option3_count += 1
        else:
            messages.warning("Sorry You cannot Vote today\n Invalid Form")
        
        poll.save()
        return redirect('poll_results')
         
    context = {'poll': poll,}
    return render(request, 'polls/votes.html', context)


# class VoteView(View):
#     template_name = 'polls/poll_vote.html'

#     def get(self, request, poll_id):
#         try:
#             poll = get_object_or_404(Polls, pk=poll_id)
#         except Polls.DoesNotExist:
#             messages.error(request, "Poll not found...")
#             return redirect('list_poll')
        
#         context = {'poll': poll}
#         return render(request, self.template_name, context)

#     def post(self, request, poll_id):
#         try:
#             poll = get_object_or_404(Polls, pk=poll_id)
#         except Polls.DoesNotExist:
#             messages.error(request, "Poll not found")
#             return redirect('list_poll')
        
#         choice = request.POST.get('poll')
        
#         if choice == 'option1':
#             poll.option1_count += 1
#         elif choice == 'option2':
#             poll.option2_count += 1
#         elif choice == 'option3':
#             poll.option3_count += 1
#         else:
#             messages.warning(request, "Sorry, you cannot vote today. Invalid Form")
        
#         poll.save()
#         messages.success(request, "Thank you for Voting...")
#         context = {'poll': poll}
#         return render(request, 'poll/poll_vote.html', context)


def results(request, pk):
    poll = Polls.objects.get(pk=pk)
    context = {
        'poll': poll,
    }
    messages.info(request, "Thank you for Voting...")
    return render(request, 'polls/results.html', context)

