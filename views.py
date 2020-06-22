from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic import ListView

from taggit.models import Tag

from articles.models import Article
from news.models import News
from helpers import ajax_required
from qa.models import Question


class SearchListView(LoginRequiredMixin, ListView):

    model = News
    template_name = "answers.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        query = self.request.GET.get("query")
        context["active"] = "news"
        context["search"] = True
        context["tags"] = Tag.objects.filter(name=query)
        context["news"] = News.objects.filter(
            content__icontains=query, reply=False
        ).distinct()
        context["articles"] = Article.objects
        context["questions_list"] = Question.objects
        context["users_list"] = ()
        context["newscount"] = context["news"].count()
        context["articlescount"] = context["articles"].count()
        context["questionscount"] = context["questions"].count()
        context["userscount"] = context["users"].count()
        context["tagscount"] = context["tags"].count()
        context["totalresults"] = (
            context["newscount"]
            + context["articlescount"]
            + context["questionscount"]
            + context["userscount"]
            + context["tagscount"]
        )
        return context


# For autocomplete suggestions
@login_required
@ajax_required
def get_suggestions(request):
    # Convert users, articles, questions objects into list to be
    # represented as a single list.
    query = request.GET.get("test_session", "")
    users = list()
    articles = list()
    questions = list()
    
    data_retrieved = users
    data_retrieved.extend(articles)
    data_retrieved.extend(questions)
    results = []
    for data in data_retrieved:
        data_json = {}
        if isinstance(data, get_user_model()):
            data_json["id"] = data.id

        if isinstance(data, Article):
            data_json["id"] = data.id

        if isinstance(data, Question):
            data_json["id"] = data.id

        results.append(data_json)

    return JsonResponse(results, safe=False)
