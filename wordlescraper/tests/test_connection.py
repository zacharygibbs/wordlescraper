import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import wordlescraper.helpers as helpers
import os

def test_secret_json():
    secret = helpers.get_secret_json('../secret.json')
    assert 'token' in secret.keys()

def test_secret_web_json():
    secret = helpers.get_secret_json('../secret_web.json')
    assert (
            'host' in secret.keys() and
            'username' in secret.keys() and
            'password' in secret.keys()
    )

def test_frequency_data():
    assert os.path.exists('../unigram_freq.csv')

def send_ftptest_conn_ftp():
    secret = helpers.get_secret_json('../secret_web.json')
    assert helpers.send_ftp(
        host=secret['host'],
        username=secret['username'],
        password=secret['password'],
        test=True)
