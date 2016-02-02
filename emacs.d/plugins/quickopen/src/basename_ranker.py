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
import re
import os
import math

class BasenameRanker(object):
  """
  Responsible for producing a ranking number for a given basename compared to a query string.

  This forms the building block for hit ordering in the upper level search systems.
  """
  def __init__(self):
    self._memoized_basic_ranks = {}

  def _is_wordstart(self, string, index):
    if index == 0:
      return True
    prev_char = string[index - 1]

    c = string[index]
    cprev = string[index - 1]
    if cprev == '_':
      return c != '_'

    if c.isupper():
      return True

    if c.isdigit() and not cprev.isdigit():
      return True

    return False

  def get_num_words(self, word):
    n = 0
    for i in range(len(word)):
      if self._is_wordstart(word, i):
        n += 1
    return n

  def get_starts(self, word):
    res = []
    for i in range(len(word)):
      if self._is_wordstart(word, i):
        res.append(i)
    return res

  def get_start_letters(self, s):
    starts = self.get_starts(s)
    s_lower = s.lower()
    return [s_lower[i] for i in starts]

  def rank_query(self, query, candidate, truncated = False, debug = False):
    basic_rank, num_word_hits = self._get_basic_rank(query, candidate, debug)[:2]

    rank = basic_rank

    # Give bonus for starting with the right letter, or for starting with the
    # right second letter.  We use the second letter because the latenc of
    # starting the open dialog sometimes causes the first letter to be dropped.
    #if len(query) >= 3 and len(candidate) >= len(query):
    #  if candidate[0] == query[0] or candidate[1] == query[0]:
    #    rank += 1

    # Give bonus for hitting all the words.
    if not truncated:
      max_num_word_hits = self.get_num_words(candidate)
      if max_num_word_hits >= 1:
        percent_hit = float(num_word_hits) / float(max_num_word_hits)
        rank += 4 * percent_hit # tune this constant

    # big points if you match the full string
    #candidatebase = os.path.splitext(candidate)[0]
    #querybase = os.path.splitext(query)[0]
    #if querybase == candidatebase:
    #  rank *= 2
    return math.floor(rank*10) / 10;

  def _get_basic_rank(self, query, candidate, debug = False):
    if debug:
      debug_data = []
      ret = self._get_basic_rank_core(debug_data, self._memoized_basic_ranks, 0, query.lower(), 0, candidate, candidate.lower())
      print "_get_basic_rank(%s, %s) -> (%s)" % (query, candidate, ret)
      print "\n".join(debug_data)
      return ret
    else:
      return self._get_basic_rank_core(None, self._memoized_basic_ranks, 0, query.lower(), 0, candidate, candidate.lower())


  def _get_basic_rank_core(self, debug_data, memoized_results, enclosing_run_length, query, candidate_index, candidate, lower_candidate):
    """
    This function tries to find the best match of the given query to the candidate. For
    a given query xyz, it considers all possible order-preserving assignments of the leters .*x.*y.*z.* into candidate.

    For these configurations, it computes a rank based on whether the matched
    letter falls on the start of a word or not.

    The highest ranked option determines the basic rank.
    """
    if len(query) == 0:
      return (0, 0)
    subcandidate = candidate[candidate_index:]
    if enclosing_run_length == 0:
      erl_type = "a"
    elif enclosing_run_length == 1:
      erl_type = "b"
    else:
      erl_type = "c"
    if query in memoized_results:
      if subcandidate in memoized_results[query]:
        if erl_type in memoized_results[query][subcandidate]:
          if debug_data:
            debug_data.append("")
            debug_data[-1] = "_get_basic_rank_core(%s,%s) -> %3.1f via cache [%s][%s]" % (
              query,
              subcandidate,
              memoized_results[query][subcandidate][erl_type][0],
              query, subcandidate
              )
          return memoized_results[query][subcandidate][erl_type]

    input_candidate_index = candidate_index
    if debug_data != None:
      debug_data.append("")
      debug_pos = len(debug_data) - 1
      #print "[%s] %30s" % ("%20s" % query, candidate[input_candidate_index:])

    # Find the best possible rank for this, memoizing results to keep
    # this from running forever.
    best_rank = 0
    for_best_rank__num_word_hits = 0
    best_debugstr = ""
    while True:
      i = lower_candidate[candidate_index:].find(query[0])
      if i == -1:
        break
      if i == 0:
        cur_run_addition = 1
        hit_first_char = True
      else:
        cur_run_addition = -enclosing_run_length # reset the enclosing_run_length
        hit_first_char = False

      i = i + candidate_index

      if self._is_wordstart(candidate, i):
        letter_rank = 2
        cur_num_word_hits = 1
      elif hit_first_char:
        # The goal of this is to rank 'ij' in 'xxxijxxx' higher than 'xxxxixxxxJxxxx'
        # Enclosing run length....
        if enclosing_run_length == 0:
          letter_rank = 1.5
        elif enclosing_run_length == 1:
          letter_rank = 2.5
        else:
          letter_rank = 3
        cur_num_word_hits = 0
      else:
        letter_rank = 1
        cur_num_word_hits = 0

      # consider all sub-interpretations...
      best_remainder_rank, remainder_num_word_hits = self._get_basic_rank_core(debug_data, memoized_results, enclosing_run_length + cur_run_addition, query[1:], i + 1, candidate, lower_candidate)

      # Update best_rank. Use word hit count to break tie so 'wvi' prefers
      # (W)eb(V)iew(I)mpl instead of (W)eb(Vi)ewImpl
      rank = letter_rank + best_remainder_rank
      num_word_hits = remainder_num_word_hits + cur_num_word_hits
      if rank > best_rank or rank == best_rank and num_word_hits > for_best_rank__num_word_hits:
        if debug_data != None:
          xxx = candidate[:i] + '*' + candidate[i+1:]
          best_debugstr = "%3.1f %s" % (best_remainder_rank, xxx)
        best_rank = rank
        for_best_rank__num_word_hits = num_word_hits
      # advance to next candidate
      candidate_index = i + 1

    if query not in memoized_results:
      memoized_results[query] = {}
    if subcandidate not in memoized_results[query]:
      memoized_results[query][subcandidate] = {}
    memoized_results[query][subcandidate][erl_type] = (best_rank, for_best_rank__num_word_hits)
    if debug_data != None:
      if best_rank > 0:
        debug_data[debug_pos] = "_get_basic_rank_core(%s,%s) -> %3.1f via %s" % (
          query, subcandidate, best_rank, best_debugstr)
      else:
        debug_data[debug_pos] = "_get_basic_rank_core(%s,%s) -> 0" % (
          query,
          subcandidate)
    return best_rank, for_best_rank__num_word_hits
