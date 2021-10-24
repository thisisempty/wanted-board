import json

from django.http           import JsonResponse
from django.views          import View
from django.db             import transaction

from core.utils            import login_decorator
from posts.models          import Post

class PostView(View):
    @login_decorator
    def post(self, request):
        data  = json.loads(request.body)
        title = data['title']
        body  = data['body']

        try :
            Post.objects.create(
                user_id = request.user.id,
                title   = title,
                body    =  body
            )

            return JsonResponse({'message' : 'SUCCESS'}, status=201)
        
        except KeyError :
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

    def get(self, request):
        limit  = int(request.GET.get('limit', 30))
        offset = int(request.GET.get('offset', 0))
        
        try :
            queryset = Post.objects.select_related('user')[offset:offset+limit]
            data = [{
                'user_id'    : post.user.account_id,
                'title'      : post.title,
                'body'       : post.body,
                'created_at' : post.created_at
            }for post in queryset]


            return JsonResponse({'count' : len(data), 'data' : data}, status=200)

        except ValueError :
            return JsonResponse({'message' : 'VALUE_ERROR'}, status=400)

    @login_decorator
    @transaction.atomic
    def patch(self, request, post_id):
        data = json.loads(request.body)

        try:
            post = Post.objects.get(id=post_id, user_id=request.user.id)

            post.title = data.get('title', post.title)
            post.body  = data.get('body', post.body)
            post.save()
        
            return JsonResponse({'message' : 'SUCCESS'}, status=400)
        
        except Post.DoesNotExist:
            return JsonResponse({'message' : 'DOES_NOT_EXIST'}, status=400)
        

    @login_decorator
    def delete(self, request, post_id):
        try:
            Post.objects.get(user_id=request.user.id, id=post_id).delete()

            return JsonResponse({'message' : 'SUCCESS'}, status=200)

        except Post.DoesNotExist:
            return JsonResponse({'message' : 'DOES_NOT_EXIST'}, status=400)

        except ValueError:
            return JsonResponse({'message' : 'VALUE_ERROR'}, status=400)

class PostDetailView(View):
    def get(self, request):
        post_id = request.GET.get('id')
        try: 
            post = Post.objects.select_related('user').get(id=post_id)

            result = {
                "user_id" : post.user.account_id,
                "title"   : post.title,
                "created_at" : post.created_at
            }
            return JsonResponse(result, status=200)

        except Post.DoesNotExist:
            return JsonResponse({'message' : 'DOES_NOT_EXIST'}, status=400)   

        except ValueError:
            return JsonResponse({'message' : 'VALUE_ERROR'}, status=400)
