# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START app]
import base64
import json
import logging
import os
import uuid
import webapp2
from datetime import datetime
from google.cloud import pubsub


class MainPage(webapp2.RequestHandler):
    def get(self):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        request_data = {}
        self.response.headers['Content-Type'] = 'text/plain'
        if 'ogid' not in self.request.cookies:
            cookie_val = str(uuid.uuid4())
            self.response.set_cookie('ogid', cookie_val, max_age=60*60*24*365)
            request_data['ogid'] = cookie_val
        else:
            request_data['ogid'] = self.request.cookies.get('ogid')


        request_data['Timestamp'] = timestamp
        request_data['User_Agent'] = self.request.headers.get('User-Agent')
        request_data['Scheme'] = self.request.scheme
        request_data['Host'] = self.request.host
        request_data['Path'] = self.request.path
        request_data['Query_String_Pairs'] = json.dumps(dict(self.request.params))
        request_data['Cookie_Pairs'] = json.dumps(dict(self.request.cookies))
        request_data['User_IP'] = self.request.remote_addr

        logging.info(self.request.headers.items())

        #for qs_pair in self.request.GET.items():
        #    request_data['Query_String_Pairs'][qs_pair[0]] = qs_pair[1]
        if self.request.referer:
            request_data['Referrer'] = self.request.referer
        else:
            request_data['Referrer'] = 'None'


        request_json = json.dumps(request_data)
        logging.info(str(request_data))

        ps = pubsub.Client()
        topic = ps.topic(os.environ['PUBSUB_TOPIC'])

        topic.publish(request_json)

        return self.response


app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
