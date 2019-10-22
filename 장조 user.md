* 장고는 User 관련 기능이 내부적으로 있다.

  -> 가져다가 쓰면 됨.

* ? django.contrib.auth.models.User 변경할 상황에서?

  -> 상속받아서 내가 만들면 됨.

  -> DB와 연결되어 있음. 다 바꿔야함. 나중에

  -> 프로젝트만들면서 미리 해라: django 추천!!

  -> 바꿨는데. 그러면 장고 내부에서 어떻게 알지? - > settings 설정의 AUTH_USER_MODEL

  -> User 클래스를 어덯게 가져다 쓰는데? -> get _user_model(): settings 설정을 봄.

* ? models.py에서도 get_user_model() 쓸 수 있음?

  -> 아닐 수 있다. 장고가 명령어를 수행할 때, INSTALLED_APPS -> models / apps

  -> User 클래스가 아직 없을 수 있다.(실행이 안되어 있을수도 있어)

  -> 그땐 그냥 settings.AUTH_USER_MODEL 로 문자열로 찍어놓으면, 알아서 바꿔준다.

* ? 근데 왜 갑자기 UserCreationForm 못씀?

  실제로 내부 코드 보면 바보 같이 User를 그대로 import 해서 씀

  (from django.contrib.auth.models import User)

  혼나야함. get_user_model() 로 써야하는데.

  그럼 어떻게 바꾼다? -> 상속 받아서 덮어쓰자.

* ! 프로젝트 시작하면 User 모델 빼자.

  User 클래스가 필요하면, get_user_model() 호출해서 쓰자.

  models.py에서만 settings.AUTH_USER_MODEL 쓰자