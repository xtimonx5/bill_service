PURCHASE_SCOPE = 'purchase'
WITHDRAWAL_SCOPE = 'withdrawal'
ACCOUNT_SCOPE = 'account'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    ]
}

OAUTH2_PROVIDER = {
    'SCOPES': {
        PURCHASE_SCOPE: 'Permission for purchase something',
        WITHDRAWAL_SCOPE: 'Permission for withdrawal',
        ACCOUNT_SCOPE: 'Check current balance & history',
    },
    'CLIENT_SECRET_GENERATOR_LENGTH': 20
}
