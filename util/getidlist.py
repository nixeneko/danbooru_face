# coding: utf-8
# IDのリストを取得
# get a list of valid ids.

JSON_DIR = "metadata"
PICKLE_FILE = "valid_ids.pickle"

import json
import glob
import os
import pickle

json_file_list = glob.glob(os.path.join(JSON_DIR, "*.json"))

valid_ids = []
for json_file in json_file_list:
    print("processing:", json_file)
    with open(json_file, 'r') as f:
        for line in f:
            j = json.loads(line)
            if not j['is_deleted'] and not j['is_banned'] and not j['is_note_locked']:
                valid_ids.append(j['id'])
            #print(j['id'], j['is_deleted'], j['is_banned'])
            #quit()
            # file_extはjpg, png等以外がくることがあるのか?要確認
#print(len(valid_ids))

with open(PICKLE_FILE, 'wb') as w:
    pickle.dump(valid_ids, w)

#rating:sに限った方がいいかも？
