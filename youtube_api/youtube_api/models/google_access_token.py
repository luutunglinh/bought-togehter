# -*- coding: utf-8 -*-

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


YOUTUBE_UPLOAD_SCOPE = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/youtube.force-ssl"
]

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


class GoogleAccessToken(models.Model):
    _name = "google.access.token"
    _description = "Google Access Token"

    name = fields.Char("User Name", required = True)
    display_name = fields.Char("Display Name")
    access_token = fields.Char("Access Token")
    access_token_expiry = fields.Datetime("Access Token Expiry")
    refresh_token = fields.Char("Refresh Token")




