from social_core.exceptions import AuthException, AuthForbidden


def associate_by_login(backend, details, user=None, *args, **kwargs):
    """
    Associate current auth with a user with the same username in the DB.
    """
    if user:
        return None

    username = details.get('username')
    if username:
        # Try to associate accounts registered with the same email address,
        # only if it's a single object. AuthException is raised if multiple
        # objects are returned.
        user_model = backend.strategy.storage.user.user_model()
        users = list(user_model.objects.filter(username=username))
        if len(users) == 0:
            return None
        elif len(users) > 1:
            raise AuthException(
                backend,
                'The given username is associated with another account',
            )
        else:
            return {'user': users[0], 'is_new': False}


class AuthForbiddenStaff(AuthForbidden):
    def __str__(self):
        return "Cannot use social log-in on staff accounts"


def protect_staff(backend, details, user=None, *args, **kwargs):
    """Prevent associating existing staff users with an authentication scheme
    out of our control.
    """
    if user and user.is_staff:
        raise AuthForbiddenStaff(backend)
