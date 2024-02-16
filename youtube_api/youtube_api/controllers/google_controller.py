import json
from odoo import http
from odoo.http import route, request, Response
import werkzeug
import traceback
import logging
import os
import httplib2
import datetime
import random
import sys
import time
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

import logging

logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)

# Explicitly tell the underlying HTTP transport library not to retry, since
# we are handling retry logic ourselves.
httplib2.RETRIES = 1

# Maximum number of times to retry before giving up.
MAX_RETRIES = 10

# Always retry when these exceptions are raised.
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError)

# Always retry when an apiclient.errors.HttpError with one of these status
# codes is raised.
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   %s

with information from the API Console
https://console.cloud.google.com/

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
"""

CLIENT_SECRETS_FILE = "client_secret.json"

YOUTUBE_UPLOAD_SCOPE = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/youtube.force-ssl"
]
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

os.path.abspath(os.path.join(os.path.dirname(__file__),
                             CLIENT_SECRETS_FILE))

VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")

RATINGS = ("like", "dislike", "none")


class YoutubeApi(http.Controller):
    @http.route('/google', auth='public', website=True)
    def google_auth(self):
        flow = self.init_google(YOUTUBE_UPLOAD_SCOPE)
        print(flow)
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='false',
            prompt='consent'
        )

        print(authorization_url, state)

        return werkzeug.utils.redirect(authorization_url)

    @staticmethod
    def init_google(scopes):
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                 CLIENT_SECRETS_FILE
                                                 ))
        flow = Flow.from_client_secrets_file(file_path, scopes=scopes)
        flow.redirect_uri = 'https://odoo.website/oath/finalize'
        client_id = request.env['ir.config_parameter'].sudo().get_param('youtube_api.google_client_id')
        client_secret = request.env['ir.config_parameter'].sudo().get_param('youtube_api.google_client_secret')
        if (not client_id) or (not client_secret):
            with open(file_path, "r") as json_file:
                client_config = json.load(json_file)
                print(client_config)
                client_id = client_config.get('web', {}).get('client_id')
                client_secret = client_config.get('web', {}).get('client_secret')
                request.env['ir.config_parameter'].sudo().set_param('youtube_api.google_client_id', client_id)
                request.env['ir.config_parameter'].sudo().set_param('youtube_api.google_client_secret', client_secret)
        return flow

    @http.route('/oath/finalize', auth='public')
    def get_youtube(self, **kw):
        print(kw)
        flow = self.init_google(kw["scope"])
        flow.fetch_token(code=kw["code"])
        credentials = flow.credentials
        print(credentials)
        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, credentials=credentials)
        print(youtube)
        youtube_request = youtube.channels().list(
            part="snippet,contentDetails,statistics",
            mine=True
        )
        res = youtube_request.execute()
        item = res.get('items')
        print(item[0])
        if item:
            snippet = item[0].get('snippet')
            name = snippet.get("customUrl")
            model_google_access = request.env['google.access.token'].sudo().search([('name', '=', name)])
            if not model_google_access:
                model_google_access.create({
                    'name': name,
                    'display_name': snippet.get('title'),
                    'access_token': credentials.token,
                    'access_token_expiry': credentials.expiry,
                    'refresh_token': credentials.refresh_token
                })
        return werkzeug.utils.redirect("/")

    @staticmethod
    def initialize_upload(args):
        data = {
            "token": args.access_token,
            "refresh_token": args.refresh_token,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "client_id": request.env['ir.config_parameter'].sudo().get_param('youtube_api.google_client_id'),
            "client_secret": request.env['ir.config_parameter'].sudo().get_param('youtube_api.google_client_secret'),
            "scopes": YOUTUBE_UPLOAD_SCOPE,
            "expiry": args.access_token_expiry.strftime("%Y-%m-%dT%H:%M:%S")
        }
        credentials = Credentials.from_authorized_user_info(data)

        return build('youtube', 'v3', credentials=credentials)

    @staticmethod
    def resumable_upload(insert_request):
        response = None
        error = None
        retry = 0
        while response is None:
            try:
                print("Uploading file...")
                status, response = insert_request.next_chunk()
                if response is not None:
                    if 'id' in response:
                        print("Video id '%s' was successfully uploaded." %
                              response['id'])
                    else:
                        exit("The upload failed with an unexpected response: %s" % response)
            except HttpError as e:
                if e.resp.status in RETRIABLE_STATUS_CODES:
                    error = "A retriable HTTP error %d occurred:\n%s" % (e.resp.status,
                                                                         e.content)
                else:
                    raise
            except RETRIABLE_EXCEPTIONS as e:
                error = "A retriable error occurred: %s" % e

            if error is not None:
                print(error)
                retry += 1
                if retry > MAX_RETRIES:
                    exit("No longer attempting to retry.")

                max_sleep = 2 ** retry
                sleep_seconds = random.random() * max_sleep
                print("Sleeping %f seconds and then retrying..." % sleep_seconds)
                time.sleep(sleep_seconds)

    @route('/test', auth='public')
    def test(self):
        upload_time = datetime.datetime(2024, 3, 8, 14, 35).isoformat()
        body = dict(
            snippet=dict(
                title='test',
                description='AMP',
                tags="travel",
                categoryId=22,

            ),
            status=dict(
                privacyStatus='private',
                publishAt=upload_time
            )
        )

        model_google_access = request.env['google.access.token'].sudo().search([('name', '=', '@luutunglinh9060')])
        youtube = self.initialize_upload(model_google_access)
        print(youtube)
        insert_request = youtube.videos().insert(
            part='snippet,status',
            body=body,
            media_body=MediaFileUpload('/home/linh/Documents/odoo-15.0/customaddons/sample_app/test.mp4', chunksize=-1,
                                       resumable=True)
        )
        self.resumable_upload(insert_request)
        return "OK"
