import sys
import string
import time
from tweepy import OAuthHandler
from tweepy import API
from tweepy import Stream
from tweepy.streaming import StreamListener

# authenticate my environment(twitter) variables
def get_twitter_auth():
    '''Setup Twitter authentication.

    Return: tweepy.OAuthHandler object
    '''
    consumer_key = 'JRMfhjfctf8riEyRHXY58iLb3'
    consumer_secret = 'OOJu2CekoR46dKuxJezo6bdqWrIIxWI7jpRiyBWitRwIy4Gs3s'
    access_token = '2383505118-VyAK1KR9Ck17IIGhdSsQNlNHK9Ki09b6DtGH3Sn'
    access_secret = 'br4zZZudQUaLtXUmN098oLqEQA1LOgtpWcpIz5mee5ris'

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    return auth

def get_twitter_client():
    '''Setup API 

    Return: tweepy.API object
    '''
    auth = get_twitter_auth()
    client = API(auth)
    return client

class CustomListener(StreamListener):
    """For streaming Twitter data."""

    def __init__(self,fname):
        safe_fname = format_filename(fname)
        self.outfile = "stream_%s.jsonl" % safe_fname

    def on_data(self,data):
        try:
            with open(self.outfile, 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            sys.sdterr.write("Error on_data: {}\n".format(e))
            time.sleep(5)
        return True

    def on_error(self, status):
        if status == 420:
            sys.stderr.write("Rate limit exceeded\n".format(status))
            return False
        else:
            sys.stderr.write("Error {}\n".format(status))
            return True

def format_filename(fname):
    """Convert fname into a safe string for a file name.

    Return: string
    """
    return ''.join(convert_valid(one_char) for one_char in fname)
def convert_valid(one_char):
    """Convert a character into '_' if "inavalid"
    
    Return: string
    """
    valid_chars = "-_.%s%s" % (string.ascii_letters, string.digits)
    if one_char in valid_chars:
        return one_char
    else:
        return '_'


if __name__ == '__main__':
    query_value = sys.argv[1:] # list of CLI arguments
    query_fname = ' '.join(query_value) # string
    auth = get_twitter_auth()
    twitter_stream = Stream(auth, CustomListener(query_fname))
    twitter_stream.filter(track=query_value, async=True)