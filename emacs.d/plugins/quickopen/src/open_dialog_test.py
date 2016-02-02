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
import db_test_base
import open_dialog
import os
import message_loop
import tempfile
import temporary_daemon
import ui_test_case

# Special indicator to TestRunner to only let us run when
# run_unit_tests is passed -m from the commandline.
requires_manual_handling = True

class FakeOptions(object):
  def __init__(self, test_data_dir):
    self.ok = True
    self.lisp_results = False
    self.results_file = None
    self.current_filename = os.path.join(test_data_dir, "project1/foo.txt")
    self.open_filenames = [os.path.join(test_data_dir, "project1/foo.txt")]

class OpenDialogTest(ui_test_case.UITestCase):
  def setUp(self):
    self.db_test_base = db_test_base.DBTestBase()
    self.db_test_base.setUp()
    self.daemon = temporary_daemon.TemporaryDaemon()
    self.db = self.daemon.db_proxy
    self.db.add_dir(self.db_test_base.test_data_dir)
    self.options = FakeOptions(self.db_test_base.test_data_dir)

  def tearDown(self):
    self.daemon.close()
    self.db_test_base.tearDown()

  def test_open_dialog(self):
    x = open_dialog.OpenDialog(self.options, self.db, "")
