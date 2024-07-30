from django.contrib.auth.tokens import PasswordResetTokenGenerator


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        """When a user registers, a unique token is generated and appended to an activation link."""
        # This method is overridden to include relevant user primary key, timestamp to ensure token expiratoion and activvity status
        # Changing password invalidates the token as well
        return str(user.pk) + str(timestamp) + str(user.is_active)


account_activation_token = AccountActivationTokenGenerator()
