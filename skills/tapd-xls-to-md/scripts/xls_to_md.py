import sys
import re
import struct

def generate_bug_list(filename):
    with open(filename, 'rb') as f:
        data = f.read()

    # Titles
    titles = []
    start = 0
    while True:
        idx = data.find(b'\x10\x30', start)
        if idx == -1: break
        
        # Check BIFF8 String Header
        # Expecting [Len][Len][Flag][Chars...]
        # idx points to first char of Chars.
        # So idx-1 is Flag. idx-3 is Len.
        if idx >= 3:
            flag = data[idx-1]
            if flag == 1: # UTF-16
                length = data[idx-3] + data[idx-2]*256
                # Sanity check length
                if 0 < length < 1000:
                    byte_len = length * 2
                    chunk = data[idx:idx+byte_len]
                    try:
                        decoded = chunk.decode('utf-16-le')
                        if 'BUG' in decoded:
                            titles.append(decoded)
                    except:
                        pass
        
        start = idx + 2
        
    dedup_titles = []
    if titles:
        dedup_titles.append(titles[0])
        for t in titles[1:]:
            if t != dedup_titles[-1]:
                dedup_titles.append(t)
    
    # IDs
    ids = []
    prefix = b'\x31\x00\x30\x00\x31\x00\x39\x00'
    start = 0
    while True:
        idx = data.find(prefix, start)
        if idx == -1: break
        chunk = data[idx+8:idx+14]
        try:
            is_digit = True
            chars = []
            for i in range(0, 6, 2):
                if chunk[i+1] != 0 or not (0x30 <= chunk[i] <= 0x39):
                    is_digit = False
                    break
                chars.append(chr(chunk[i]))
            if is_digit:
                 uid = "1019" + "".join(chars)
                 ids.append(uid)
        except:
             pass
        start = idx + 2
    
    dedup_ids = []
    seen_ids = set()
    for i in ids:
        if i not in seen_ids:
            dedup_ids.append(i)
            seen_ids.add(i)

    # Output
    count = 1
    limit = min(len(dedup_titles), len(dedup_ids))
    
    for i in range(limit):
        raw = dedup_titles[i]
        uid = dedup_ids[i]
        
        clean_title = raw.replace('【BUG】', '')
        
        clean_title = clean_title.strip()
        
        long_id = "116823115600" + uid
        url = f"https://www.tapd.cn/68231156/bug/detail/{long_id}"
        
        line = f"{count}: {clean_title}{uid}【{clean_title}】{url}"
        print(line)
        count += 1

if __name__ == "__main__":
    generate_bug_list(sys.argv[1])
