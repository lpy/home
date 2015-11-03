#!/bin/sh

echo "Executing auto compilation mission daily"
echo `date`
cd `cat ~/.markutils/m0`
echo "Begin to compile"
git rebase-update && cd .. && gclient sync && cd src/ && ninja -C out/Release -j96
echo "DONE"
echo `date`
