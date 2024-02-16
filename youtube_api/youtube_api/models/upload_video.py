# -*- coding: utf-8 -*-
import base64
import pathlib

from odoo import models, fields, api
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
from googleapiclient.http import MediaIoBaseUpload
from odoo.exceptions import ValidationError
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


class UploadYoutube(models.Model):
    _name = "upload.video"
    _description = "upload video youtube"

    name = fields.Char("Title")
    description = fields.Text("Description")
    categoryId = fields.Char("Category Id")
    tags = fields.Char("Tags")
    publishAt = fields.Datetime('publish At')
    isPublish = fields.Boolean("is Publish", default=False, readonly=True)
    channel = fields.Many2one('google.access.token', string="Youtube Channel")
    video_file = fields.Binary("Video file")

    def upload_video(self):
        client_id = self.env['ir.config_parameter'].sudo().get_param('youtube_api.google_client_id')
        client_secret = self.env['ir.config_parameter'].sudo().get_param('youtube_api.google_client_secret')
        body = {
            'snippet': {
                'categoryId': self.categoryId,
                'title': self.name,
                'description': self.description,
                'tags': self.tags,
            },
            'status': {
                'privacyStatus': 'private',
                'publishAt': self.publishAt.isoformat(),
            }
        }

        youtube = self.initialize_upload(self.channel, client_id, client_secret)
        print(youtube)
        file_path = self.get_video()
        insert_request = youtube.videos().insert(
            part='snippet,status',
            body=body,
            media_body=MediaFileUpload(file_path,
                                       chunksize=-1,
                                       resumable=True)
        )

        self.resumable_upload(insert_request)

    def get_video(self):
        decoded_video_data = base64.b64decode(self.video_file)
        input_file = f'{pathlib.Path(__file__).parent.parent}'
        print(input_file)
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        video_filename = f'uploaded_video_{timestamp}.mp4'
        video_path = f'{pathlib.Path(__file__).parent.parent}/static/{video_filename}'
        with open(video_path, 'wb') as video_file:
            video_file.write(decoded_video_data)
        video_file.close()
        return video_path

    @staticmethod
    def initialize_upload(args, client_id, client_secret):
        data = {
            "token": args.access_token,
            "refresh_token": args.refresh_token,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "client_id": client_id,
            "client_secret": client_secret,
            "scopes": YOUTUBE_UPLOAD_SCOPE,
            "expiry": args.access_token_expiry.strftime("%Y-%m-%dT%H:%M:%S")
        }
        credentials = Credentials.from_authorized_user_info(data)

        return build('youtube', 'v3', credentials=credentials)

    def resumable_upload(self, insert_request):
        response = None
        error = None
        retry = 0
        while response is None:
            try:
                print(
                    "Up0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000                                 loading file...")
                status, response = insert_request.next_chunk()
                if response is not None:
                    if 'id' in response:
                        print("Video id '%s' was successfully uploaded." %
                              response['id'])
                        result = 'Success'
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

        if result == 'Success':
            self.isPublish = True
        else:
            raise ValidationError(f"{result}")
