from django.shortcuts import render, redirect

# Create your views here.
from .forms import *
from .models import *

from django.core.paginator import Paginator




# 전체 화면과 생성하기
def board(request):
    if request.method == 'POST':
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

    else:
        page = request.GET.get('page', '1')
        board = Board.objects.all()

        paginator = Paginator(board, 5)
        page_obj = paginator.get_page(page)

        context = {
            'board': page_obj
        }
        return render(request, 'board.html', context)


# 수정
def boardEdit(request, pk):
    board = Board.objects.get(id=pk)
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
    else:
        boardForm = BoardForm
        return render(request, 'create.html', {'boardForm': boardForm})


# 삭제
def boardDelete(request, pk):
    board = Board.objects.get(id=pk)
    board.delete()
    return redirect('board')

def dDetail(request, pk):
    board = Board.objects.get(id=pk)
    return render(request, 'detail.html', {'board': board})