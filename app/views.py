from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response
from .models import STATUS,Category,Comment,Post,Like
from rest_framework import status
from .serializers import(
    CategorySerializer,
    CommentSerializer,
    LikeSerailizer,
    PostSerializer,
    PostvaluesSerializer,
)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    @action(detail=False,methods=['POST'])
    def create_data(self,request,*args, **kwargs):
        data = self.serializer_class(data=request.data or None)
        data.is_valid(raise_exception=True)

        title = data.validated_data.get('title')
        slug = data.validated_data.get('slug')
        description = data.validated_data.get('description')

        obj= Category.objects.create(title=title,slug=slug,description=description)
        serializer = self.serializer_class(obj)
        return Response({'status':False,'data':serializer.data,'message':"data successfully created"},status=status.HTTP_201_CREATED)


    @action(detail=False,methods=['POST'])
    def save_data(self,request,*args, **kwargs):
        data = self.serializer_class(data =request.data)
        data.is_valid(raise_exception=True)

        title_data = data.validated_data.get('title')
        slug_data = data.validated_data.get('slug') 
        description_data = data.validated_data.get('description')

        obj =Category()
        obj.title = title_data
        obj.slug = slug_data
        obj.description = description_data
        obj.save()
        serializer = self.serializer_class(obj)
        return Response({'status':False,'data':serializer.data,'message':"data successfully created"})


    @action(detail=False,methods=['POST'])
    def get_or_create(self,request,*args, **kwargs):
        data =self.serializer_class(data = request.data)
        data.is_valid(raise_exception=True)
        title_data = data.validated_data.get('title')
        slug_data = data.validated_data.get('slug')

        obj,_ = Category.objects.get_or_create(title=title_data,slug=slug_data)
        serializer = self.serializer_class(obj)
        return Response({'status':False,'data':serializer.data,'message':"data successfullt created"},status=status.HTTP_201_CREATED)
    
    @action(detail=False,methods=['POST'])
    def bulk_create(self,request,*args, **kwargs):
        data = self.serializer_class(data = request.data,many=True)
        data.is_valid(raise_exception=True)
        new_data = []
        for row in data.validated_data:
            obj =Category(title = row.get('title'),
            slug = row.get('slug'),
            description = row.get('description')
            )
            new_data.append(obj)
            print("New data",new_data)

        if new_data:
            new_data = Category.objects.bulk_create(new_data)
           
        return Response({'status':False,'message':"data successfully Crated"},status=status.HTTP_201_CREATED)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerailizer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    @action(detail=True,methods=['PATCH'])
    
    def add_category(self,request,pk,*args, **kwargs):
        categories = request.data.get('ids')
        print("ID -->",categories)
        instance =Post.objects.filter(pk=pk).first()
        categories = set(categories)
        instance.category.add(*categories)

        serializer = self.serializer_class(instance)
        return Response(serializer.data,status=status.HTTP_200_OK)

    @action(detail=True,methods=['PATCH'])
    def set_category(self,request,pk,*args, **kwargs):
        categories = request.data.get('ids')
        print("ID -->",categories)
        instance =Post.objects.filter(pk=pk).first()

        instance.category.set(categories)

        serializer = self.serializer_class(instance)
        return Response(serializer.data,status=status.HTTP_200_OK)

    @action(detail=True,methods=['POST'])
    def update_data(self,request,pk,*args, **kwargs):
        summary_data = request.data.get('summary')
        content_data =request.data.get('content')
        Post.objects.filter(pk=pk).update(summary=summary_data,content=content_data)
        return Response({'message':'successfully updated the data'})
    @action(detail=False,methods=['POST'])
    def update_or_create(self,request,*args, **kwargs):
        categoty_data = set(request.data.get('category'))
        summary_data = request.data.get('summary')
        title_data = request.data.get('title')
        author =1
        content_data = request.data.get('content')

        obj,_ = Post.objects.update_or_create(title=title_data,
        defaults={
            'summary':summary_data,
            'content':content_data,
            'author_id':author
        }
        )
        obj.category.set(categoty_data)
        return Response({'message':"Successfully updated the data"})

    @action(detail=False,methods=['POST'])
    def bulk_update(self,request,*args, **kwargs):
        ids = request.data.get('ids')

        queryset = Post.objects.filter(id__in=ids)

        for obj in queryset:
           obj.status = STATUS.PUBLISH.value
        Post.objects.bulk_update(queryset,['status'])
        return Response({'message':'sucessfully updated the data'})


    @action(detail=False,methods=['GET'])
    def get_all(self,request,*args, **kwargs):
        queryset = Post.objects.all()
        serializer = self.serializer_class(queryset,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    @action(detail=False,methods=['GET'])
    def get_one(self,request,*args, **kwargs):
        slug = request.GET.get("slug")

        try:
            obj = Post.objects.get(slug=slug)
        except Post.MultipleObjectsReturned:
            return Response({
                "message":"Multiple objects found"
            },status=status.HTTP_400_BAD_REQUEST)
        except Post.DoesNotExist:
            return Response({
                "message":"Object not found"
            },status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(obj)
        return Response(serializer.data,status=status.HTTP_200_OK)
    @action(detail=False,methods=['GET'])
    def exclude_filter(self,request,*args, **kwargs):
        id = request.GET.get('id')
        queryset = Post.objects.exclude(id =id)
        serializer = self.serializer_class(queryset,many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)
    @action(detail=False,methods=['GET'])
    def limit_data(self,request,*args, **kwargs):
        queryset = Post.objects.all()[:1]
        serializer = self.serializer_class(queryset,many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)
    @action(detail=False,methods=['GET'])
    def lookup_filter(self,request,*args, **kwargs):
        ids = request.GET.get('ids')
        ids = ids.split(',')
        queryset  = Post.objects.filter(id__in=ids)
        serializer = self.serializer_class(queryset,many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)

    

        