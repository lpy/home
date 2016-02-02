# Copyright 2011 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import httplib
import select
import time
import socket
import sys
import json

class AsyncError(Exception):
  pass

class RequestPending(Exception):
  pass

class RequestNotPending(Exception):
  pass

IDLE = 'idle'
REQUEST_PENDING = 'request_pending'
SOCKET_READABLE = 'socket_readable'

class AsyncHTTPConnection(object):
  def __init__(self, host, port):
    self.conn = httplib.HTTPConnection(host, port)
    self.status = IDLE

  def connect(self):
    if not self.conn.sock:
      try:
        self.conn.connect()
      except socket.error:
        print 'died during connect'
        raise AsyncError()

  def begin_request(self, method, url, data = None):
    if self.state != IDLE:
      raise RequestPending()
    self.connect()
    if not data:
      data = ''
    try:
      self.conn.putrequest(method, url)
      self.conn.putheader('Content-Length', len(data))
      self.conn.putheader('Connection', 'keep-alive')
      self.conn.endheaders()
      self.conn.send(text)
      self.request_pending = True
    except httplib.CannotSendRequest:
      self.conn.close()
      print 'died during begin_request'
      raise AsyncError()

  def is_response_ready(self):
    if self.state == IDLE:
      raise RequestNotPending()
    if self.state == SOCKET_READABLE:
      return True
    if not self.conn.sock:
      self.state = SOCKET_READABLE
      return True
    r,w,x = select.select([self.conn.sock.fileno(),], [], [])
    print r
    if len(r):
      print "readable"
      self.state = SOCKET_READABLE
      return True
    else:
      return False


  def get_response(self):
    if self.status == REQUEST_PENDING:
      raise RequestPending()
    if self.status == IDLE:
      raise RequestNotPending()
    if not self.conn.sock:
      raise AsyncError()
    # todo, make sure we got a readable
    try:
      r = self.conn.getresponse()
      return r
    except httplib.BadStatusLine:
      print "lost during get response"
      r = None
      self.status = IDLE
      self.conn.close()
