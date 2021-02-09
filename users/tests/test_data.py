from django.contrib.auth import get_user_model

UserModel = get_user_model()


def create_user_jake():
    user = UserModel.objects.create_user(
        email="jake.peralta@b99.com", username='baracuda',
        first_name="Jake", last_name="Peralta", password='rosa1234'
    )
    return user


def create_user_amy():
    user = UserModel.objects.create_user(
        email="amy.santiago@b99.com", username='Aby',
        first_name="Amy", last_name="Santiago", password='philatelie'
    )
    return user


def create_inactive_user():
    user = UserModel.objects.create_user(
        email="norm.scully@b99.com", username='Norm',
        first_name="Norm", last_name="Scully", password='1234',
        is_active=False
    )
    user.generate_validation_token()
    return user
