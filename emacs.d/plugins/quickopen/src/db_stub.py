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
import daemon
import db
import re
import time
import urlparse

from trace_event import *
from query import Query


# TODO(nduca): is Stub the right word for this class? Mehh
class DBStub(object):
  def __init__(self, settings, server):
    self.db = db.DB(settings)
    self.db.needs_indexing.add_listener(self.on_db_needs_indexing)
    self.server = server

    server.add_json_route('/begin_reindex', self.begin_reindex, ['POST'])
    server.add_json_route('/dirs/add', self.add_dir, ['POST'])
    server.add_json_route('/dirs', self.list_dirs, ['GET'])
    server.add_json_route('/dirs/([a-zA-Z0-9]+)', self.get_dir, ['GET'])
    server.add_json_route('/dirs/([a-zA-Z0-9]+)', self.delete_dir, ['DELETE'])
    server.add_json_route('/ignores', self.get_ignores, ['GET'])
    server.add_json_route('/ignores/add', self.ignores_add, ['POST'])
    server.add_json_route('/ignores/remove', self.ignores_remove, ['POST'])
    server.add_json_route('/sync', self.sync, ['POST'])
    server.add_json_route('/status', self.status, ['GET'])
    server.add_json_route('/search(.*)', self.search, ['POST'])
    server.add_json_route('/get_oauth', self.get_oauth, ['GET'])
    server.add_json_route('/set_oauth', self.set_oauth, ['POST'])
    if not self.db.is_up_to_date:
      self.on_db_needs_indexing()

  def on_db_needs_indexing(self):
    self.server.add_delayed_task(self._index_a_bit_more, 0.05)

  def _index_a_bit_more(self):
    if not self.db.is_up_to_date:
      # enqueue the task before, so we dont get a stall.
      self.server.add_delayed_task(self._index_a_bit_more, 0.25)
      self.db.step_indexer()

  def add_dir(self, m, verb, data):
    d = self.db.add_dir(data["path"])
    return {"id": d.id,
            "status": 'OK'}

  def list_dirs(self, m, verb, data):
    return map(lambda d: d.__getstate__(), self.db.dirs)

  def get_dir(self, m, verb, data):
    id = m.group(1)
    for d in self.db.dirs:
      if d.id == id:
        return d.__getstate__()
    raise daemon.NotFoundException()

  def delete_dir(self, m, verb, data):
    id = m.group(1)
    for d in self.db.dirs:
      if d.id == id:
        self.db.delete_dir(d)
        return {"status": 'OK'}
    raise daemon.NotFoundException()

  def get_ignores(self, m, verb, data):
    return self.db.ignores

  def ignores_add(self, m, verb, data):
    self.db.ignore(data)
    return {"status": "OK"}

  def ignores_remove(self, m, verb, data):
    try:
      self.db.unignore(data)
    except Exception:
      raise daemon.SilentException()
    return {"status": "OK"}

  @traced
  def search(self, m, verb, data):
    query = Query.from_dict(data)
    return self.db.search(query).as_dict()

  @traced
  def sync(self, m, verb, data):
    self.db.sync()
    return {"status": "OK"}

  @traced
  def status(self, m, verb, data):
    return self.db.status().as_dict()

  def begin_reindex(self, m, verb, data):
    self.db.begin_reindex()
    return {"status": "OK"}

  def set_oauth(self, m, verb, data):
    if not 'token' in data:
      raise daemon.SilentException()
    self.db.token = str(data['token'])
    return {"status": "OK"}

  def get_oauth(self, m, verb, data):
    token = self.db.token
    if not token:
      return {}
    return {'token': token}
