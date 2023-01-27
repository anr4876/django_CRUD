import datetime
from datetime import date
from datetime import datetime
from django.shortcuts import render, redirect

# Create your views here.
from .forms import *
from .models import *
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import urllib
import os
from django.http import HttpResponse, Http404, response
import mimetypes
from django.shortcuts import get_object_or_404
import csv


# =================================================================================================================
# 메인 화면 생성
# =================================================================================================================


# 전체 화면과 생성하기
def board(request):
    page = request.GET.get('page', '1')
    kw = request.GET.get('keyword', '')
    list_s = request.GET.get('list_s')

    trip_start = request.GET.get('trip_start', '')
    trip_last = request.GET.get('trip_last', '')
    start = '2023-01-01'
    if trip_last == "":
        trip_last = date.today()
    if trip_start == "":
        trip_start = start

    # search_type = request.GET.get('type', '')


    if kw:

        if list_s == 'all_list':
            board = Board.objects.filter(board_time__range=[trip_start, trip_last]).filter(
                Q(title__icontains=kw) |  # 제목 검색
                Q(content__icontains=kw)
            ).distinct()

        elif list_s == 'name':
            board = Board.objects.filter(board_time__range=[trip_start, trip_last]).filter(
                Q(title__icontains=kw)   # 제목 검색
            ).distinct()

        elif list_s == 'content':
            board = Board.objects.filter(board_time__range=[trip_start, trip_last]).filter(
                Q(content__icontains=kw)
            ).distinct()

    else:

        board = Board.objects.filter(board_time__range=[trip_start, trip_last]).all().order_by('-list_num')

    bd = board.count()
    paginator = Paginator(board, 8)
    page_obj = paginator.get_page(page)

    context = {
        'board': page_obj,
        'bd': bd,
        'keyword': kw,
    }
    return render(request, 'board.html', context)


# =================================================================================================================
# /메인 화면 생성
# =================================================================================================================


# =================================================================================================================
# 엑셀 다운로드 기능
# =================================================================================================================

def ex_download_view(request, pk):
    board = get_object_or_404(Board, pk=pk)

    f = open(board.title + ".csv", "wt", newline='', encoding="utf-8-sig")

    wr = csv.writer(f)

    wr.writerow(['제목', '작성자', '작성 일자', '내용'])
    wr.writerow([board.title, board.user, board.board_time, board.content])

    f.close()

    url ="C:\CRUD_Project/" + board.title + ".csv"
    file_url = urllib.parse.unquote(url)

    if os.path.exists(file_url):
        with open(file_url, 'rb') as fh:
            quote_file_url = urllib.parse.quote(board.title.encode('utf-8')) + '.csv'
            print(quote_file_url)
            response = HttpResponse(fh.read(), content_type=mimetypes.guess_type(file_url)[0])
            response['Content-Disposition'] = 'attachment;filename*=UTF-8\'\'%s' % quote_file_url
            return response
        raise Http404

# =================================================================================================================
# /엑셀 다운로드 기능
# =================================================================================================================



# =================================================================================================================
# 수정 화면 생성
# =================================================================================================================


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


# =================================================================================================================
# /수정 화면 생성
# =================================================================================================================


# =================================================================================================================
# 생성 화면 생성
# =================================================================================================================

# 생성
def boardCreate(request):
    now = datetime.now()
    if request.method == 'POST':
        try:
            title = request.POST['title']
            content = request.POST['content']
            user = request.user
            filename = None
            upload_files = None
            file_now = "media/{}/{}/{}/{}{}{}".format(now.year, now.month, now.day, now.hour, now.minute, now.second)
            if request.FILES:
                files = request.FILES['upload_files']
                fs = FileSystemStorage(location=file_now, base_url=file_now)
                filename = fs.save(files.name, files)
                upload_files = fs.url(filename)

            board = Board(
                title=title,
                content=content,
                user=user,
                filename=filename,
                upload_files=upload_files,
            )
            board.save()
            return redirect('board')
        except:
            return render(request, 'create.html')
    else:
        boardForm = BoardForm
        return render(request, 'create.html', {'boardForm': boardForm})


# =================================================================================================================
# /생성 화면 생성
# =================================================================================================================


# =================================================================================================================
#  데이터베이스 칼럼 삭제 구현
# =================================================================================================================


# 삭제
def boardDelete(request, pk):
    board = Board.objects.get(list_num=pk)
    if request.user == board.user:
        board.delete()
    else:
        messages.warning(request, "권한이 없습니다.")

    return redirect('board')


# =================================================================================================================
#  /데이터베이스 칼럼 삭제 구현
# =================================================================================================================

# =================================================================================================================
#  자세히 보기 화면 생성
# =================================================================================================================

def dDetail(request, pk):
    board = Board.objects.get(list_num=pk)
    return render(request, 'detail.html', {'board': board})


# =================================================================================================================
#  /자세히 보기 화면 생성
# =================================================================================================================


# =================================================================================================================
#  로그인이 되어있는 사용자만 사용 가능한 기능 구현
# =================================================================================================================


def login_message_required(function):
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, "로그인한 사용자만 이용할 수 있습니다.")
            return redirect(settings.LOGIN_URL)
        return function(request, *args, **kwargs)

    return wrap


# =================================================================================================================
#  /로그인이 되어있는 사용자만 사용 가능한 기능 구현
# =================================================================================================================


# =================================================================================================================
#  파일 다운로드 기능 구현
# =================================================================================================================


@login_message_required
def board_download_view(request, pk):
    board = get_object_or_404(Board, pk=pk)
    url = board.upload_files.url[1:]
    file_url = urllib.parse.unquote(url)
    
    if os.path.exists(file_url):
        with open(file_url, 'rb') as fh:
            quote_file_url = urllib.parse.quote(board.filename.encode('utf-8'))
            response = HttpResponse(fh.read(), content_type=mimetypes.guess_type(file_url)[0])
            response['Content-Disposition'] = 'attachment;filename*=UTF-8\'\'%s' % quote_file_url
            return response
        raise Http404

# =================================================================================================================
#  /파일 다운로드 기능 구현
# =================================================================================================================
