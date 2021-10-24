import json, bcrypt, re, jwt

from django.http import JsonResponse
from django.views import View

from wanted.settings import ALGORITHM, SECRET_KEY
from users.models import User

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)

        account_id = data['account_id']
        password   = data['password']

        REGEX_PASSWORD = '^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).{8,}'
        ACCOUNT_ID_REGEX  = "^[a-z0-9+-_.]"

        if not re.match(REGEX_PASSWORD, password):
            return JsonResponse({'message': 'INVAILD_PASSWORD'}, status=400)
            
        if not re.match(ACCOUNT_ID_REGEX, account_id):
            return JsonResponse({'message': 'INVAILD_ID'}, status=400)

        try:
            if User.objects.filter(account_id=account_id).exists():
                return JsonResponse({'message': 'ALREADY_EXISTS'}, status=400)

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            decoded_password = hashed_password.decode('utf-8')

            User.objects.create(
                account_id = account_id,
                password   = decoded_password
            )
            return JsonResponse({'message' : 'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400) 

class SignInView(View):
    def get(self, request):
        try :
            data = json.loads(request.body)

            account_id = data['account_id']
            password   = data['password']

            user = User.objects.get(account_id=account_id)

            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({'MESSAGE' : 'INVALID_PASSWORD'}, status = 401)
            
            access_token = jwt.encode({'id' : user.id}, SECRET_KEY, algorithm=ALGORITHM)

            return JsonResponse({'ACCESS_TOKEN' : access_token}, status = 200)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
        
        except User.DoesNotExist:
            return JsonResponse({'message' : 'DOES_NOT_EXIST'}, status=400)
