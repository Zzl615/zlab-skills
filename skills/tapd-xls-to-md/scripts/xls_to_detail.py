import sys
import struct

def xls_to_detail(filename):
    with open(filename, 'rb') as f:
        data = f.read()

    # 1. Find all strings
    all_strings = {}
    
    start = 0
    # Scan for Header: [Len][Len][Flag=01]
    while True:
        idx = data.find(b'\x01', start)
        if idx == -1: break
        
        if idx >= 2:
            length = data[idx-2] + data[idx-1]*256
            if 0 < length < 32000: # Max Excel string length check
                byte_len = length * 2
                chunk_start = idx + 1
                chunk_end = chunk_start + byte_len
                
                # Check bounds
                if chunk_end <= len(data):
                    try:
                        chunk = data[chunk_start:chunk_end]
                        s = chunk.decode('utf-16-le')
                        all_strings[chunk_start] = s
                        start = chunk_end
                        continue
                    except:
                        pass
        start = idx + 1
    
    sorted_offsets = sorted(all_strings.keys())
    
    # 2. Identify Titles
    titles = []
    for off in sorted_offsets:
        s = all_strings[off]
        # Use regex or simple check
        if '【BUG】' in s: 
             titles.append(off)
             
    # Dedup consecutive titles (same content next to each other)
    dedup_titles = []
    if titles:
        dedup_titles.append(titles[0])
        for t in titles[1:]:
             if all_strings[t] != all_strings[dedup_titles[-1]]:
                 dedup_titles.append(t)
    
    # 3. Process each bug
    current_iteration = "未知迭代"
    last_printed_iteration = None
    
    for i, t_off in enumerate(dedup_titles):
        title_str = all_strings[t_off]
        
        # Range: from this Title to next Title (or EOF)
        start_range = t_off
        end_range = dedup_titles[i+1] if i+1 < len(dedup_titles) else 999999999
        
        # Find strings in this range
        bug_content = []
        for off in sorted_offsets:
            if start_range < off < end_range:
                bug_content.append(all_strings[off])
        
        # Parse fields
        description = "无详细描述"
        comment = "无评论"
        
        for s in bug_content:
            # Comment check
            if '【评论' in s:
                comment = s
            # Iteration check: short, often "AI..." or known list
            # Heuristic: shorter than 30 chars, contains "AI" or "迭代" or looks like version "x.x"
            elif len(s) < 30 and ('AI' in s or '迭代' in s or any(char.isdigit() for char in s)):
                # Update sticky iteration
                current_iteration = s
            # Description check
            # Usually the longest remaining string, or starts with [描述]
            elif '[描述]' in s or '提供信息' in s:
                 description = s
            elif description == "无详细描述" and len(s) > 50:
                 # Fallback: take long string as description
                 description = s
                 
        # Format Output
        clean_title = title_str.replace('【BUG】', '').strip()
        
        # Iteration Header
        if current_iteration != last_printed_iteration:
            print(f"# {current_iteration}")
            last_printed_iteration = current_iteration
            
        print(f"## {clean_title}")
        print(f"1. {description.strip()}")
        print(f"2. {comment.strip()}")
        print("") # Extra newline for spacing

if __name__ == "__main__":
    xls_to_detail(sys.argv[1])
