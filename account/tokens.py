from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type                                                           # generator reset password


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    """
    Gernerate token
    """
    def _make_hash_value(self, user, timestamp):
        """
        Combines the user's primary key (user.pk), the current timestamp, and the user's is_active status to create a unique hash value for the token
        """
        return (
            text_type(user.pk) + text_type(timestamp) + text_type(user.is_active)
        )


account_activation_token = AccountActivationTokenGenerator()