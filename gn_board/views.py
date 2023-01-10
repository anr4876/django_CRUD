from django.shortcuts import render, redirect

# Create your views here.
from .forms import *
from .models import *
from django.db import connection
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q



# 전체 화면과 생성하기
def board(request):



    if request.method == 'POST':
        title = request.POST['title']
        board_time = request.POST['board_time']
        user = request.user
        list_num = request.POST['list_num']

        board = Board(
            title=title,
            board_time=board_time,
            user=user,
            list_num=list_num,
        )
        board.save()
        return redirect('board')

    else:
        page = request.GET.get('page', '1')
        kw = request.GET.get('keyword', '')
        #search_type = request.GET.get('type', '')




        if kw :
            board = Board.objects.filter(
                Q(title__icontains=kw) |  # 제목 검색
                Q(content__icontains=kw)

            ).distinct()


        else:
            board = Board.objects.all().order_by('-list_num')

        bd = board.count()
        paginator = Paginator(board, 8)
        page_obj = paginator.get_page(page)

        context = {
            'board': page_obj,
            'bd':bd,
            'keyword':kw,
        }
        return render(request, 'board.html', context)




# 수정
def boardEdit(request, pk):
    board = Board.objects.get(list_num=pk)
    if request.user != board.user:
        messages.warning(request, "권한이 없습니다.")
        return redirect('board')
    else:
        if request.method == "POST":
            board.title = request.POST['title']
            board.content = request.POST['content']
            board.user = request.user

            board.save()
            return redirect('board')

        else:
            boardForm = BoardForm(instance=board)
            return render(request, 'update.html', {'boardForm': boardForm})


# 생성
def boardCreate(request):
    if request.method == 'POST':
        try:
            title = request.POST['title']
            content = request.POST['content']
            user = request.user

            board = Board(
                title=title,
                content=content,
                user=user,
            )
            board.save()
            return redirect('board')
        except:
            return render(request, 'create.html')
    else:
        boardForm = BoardForm
        return render(request, 'create.html', {'boardForm': boardForm})


# 삭제
def boardDelete(request, pk):

    board = Board.objects.get(list_num=pk)
    if request.user == board.user:
        board.delete()
    else:
        messages.warning(request, "권한이 없습니다.")

    return redirect('board')

def dDetail(request, pk):
    board = Board.objects.get(list_num=pk)
    return render(request, 'detail.html', {'board': board})