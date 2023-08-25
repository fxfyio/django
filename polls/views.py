from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.urls import reverse


def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/index.html", context)


def detail(request, question_id):
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")
    # return render(request, "polls/detail.html", {"question": question})
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):  # 定义投票视图，需要request对象和问题ID作为参数
    question = get_object_or_404(
        Question, pk=question_id)  # 尝试获取问题对象，如果没有找到，返回404错误

    try:
        selected_choice = question.choice_set.get(
            pk=request.POST["choice"])  # 尝试获取选中的选项，使用POST中的“choice”值
    except (KeyError, Choice.DoesNotExist):  # 如果未找到选项或未选择选项，则捕获异常
        return render(  # 返回详细页面，并显示错误消息
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice."
            },
        )
    else:
        selected_choice.votes += 1  # 如果找到选项，则增加投票数
        selected_choice.save()  # 保存选项对象，以更新数据库中的投票数
        # 重定向到结果页面
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
