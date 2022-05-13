import jwt
import pytz
import os
import rsa
import dotenv
import tweepy
from base.models import Organisation, User
from django.conf import settings

dotenv_file = os.path.join(settings.BASE_DIR, ".env")
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)


def getUser(token):
    decodedToken = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    user = User.objects.get(id=decodedToken['user_id'])

    return user


def genErrorMsg(message):
    return 'Error {}. Please contact customer care for assistance'.format(message)


def genDateTimeString(dateObj):
    naiTimeZone = pytz.timezone("Africa/Nairobi")
    naiTime = dateObj.astimezone(naiTimeZone)
    dateString = naiTime.strftime("%a, %d %b %Y at %I:%M:%S%p")

    return dateString


def getPrivateKey():
    privateKey = rsa.PrivateKey(int(os.environ.get('N')), int(os.environ.get('E')), int(
        os.environ.get('D')), int(os.environ.get('P')), int(os.environ.get('Q')))

    return privateKey


def genTweepyAuthAndCallAPI(page):
    # get encrypted user data
    pk = getPrivateKey()
    customerKey = rsa.decrypt(page['data']['twitter_api_key'], pk).decode()
    customerSecret = rsa.decrypt(
        page['data']['twitter_api_key_secret'], pk).decode()
    access_key = rsa.decrypt(
        page['data']['twitter_access_key_secret'], pk).decode()
    access_key_secret = rsa.decrypt(
        page['data']['twitter_access_key_secret'], pk).decode()
    bearer_token = rsa.decrypt(
        page['data']['twitter_bearer_token'], pk).decode()

    auth = tweepy.OAuthHandler(customerKey, customerSecret)
    auth.set_access_token(access_key, access_key_secret)

    return tweepy.API(auth)
