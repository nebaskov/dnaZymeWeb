from django.shortcuts import render


def knowledgebase(request):
    return render(request, 'main/knowledgebase.html')


def article_1(request):
    return render(request, 'main/article_1.html')


def article_2(request):
    return render(request, 'main/article_2.html')


def article_3(request):
    return render(request, 'main/article_3.html')


def article_4(request):
    return render(request, 'main/article_4.html')


def article_5(request):
    return render(request, 'main/article_5.html')


def article_6(request):
    return render(request, 'main/article_6.html')


def article_7(request):
    return render(request, 'main/article_7.html')


def article_8(request):
    return render(request, 'main/article_8.html')
