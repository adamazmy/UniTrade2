                    ###   AUTHOR: ZIYAD ELGYZIRI   ###


from django.contrib.auth.tokens import PasswordResetTokenGenerator

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # No need for text_type, directly use user.pk and timestamp
        return str(user.pk) + str(timestamp)


generate_token = TokenGenerator()
