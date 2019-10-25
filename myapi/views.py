from rest_framework import viewsets
from .models import Essay, Album, Files
from .serializers import EssaySerializer, AlbumSerializer, FilesSerializer

# 파일 업로드 문제 해결
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination

class MyPagination(PageNumberPagination):
    page_size = 1

class PostViewSet(viewsets.ModelViewSet):

    queryset = Essay.objects.all()
    serializer_class = EssaySerializer
    pagination_class = MyPagination

    filter_backends = [SearchFilter]
    search_fields = ('title', 'body')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        qs = super().get_queryset()

        if self.request.user.is_authenticated:
            if self.request.user.is_staff:
                pass
            else:
                qs = qs.filter(author = self.request.user)
        else:
            qs = qs.none()

        return qs

class ImgViewSet(viewsets.ModelViewSet):
    
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

class FileViewSet(viewsets.ModelViewSet):
    
    queryset = Files.objects.all()
    serializer_class = FilesSerializer

    # 파일 업로드 문제를 해결하기 위한 방법
    # 1. parser_class 지정
    # 2. create() 오버라이딩

    # 파일 업로드 문제 해결 다양한 미디어 파일로 리퀘스트를 수락하는 방법
    parser_classes = (MultiPartParser, FormParser)

    # create() -> post()

    def post(self, request, *args, **kwargs):
        serializer = FilesSerializer(data=request.data)
        if seializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.error, status=HTTP_400_BAD_REQUEST)