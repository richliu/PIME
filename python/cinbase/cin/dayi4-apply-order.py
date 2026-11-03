# 依 dayi4-order-recommend.txt 的標籤，重排 dayi4.cin 候選字順序並合併 MERGE 字，輸出新檔
import re, sys
from collections import OrderedDict, defaultdict
cin_in, rec_in, cin_out, report_out = sys.argv[1:5]
def big5(c):
    try: c.encode('big5'); return True
    except: return False
def gb(c):
    try: c.encode('gb2312'); return True
    except: return False
lines = open(cin_in, encoding='utf8').read().split('\n')
# chardef 範圍與每鍵的行索引
beg = next(i for i, l in enumerate(lines) if l.startswith('%chardef begin'))
end = next(i for i, l in enumerate(lines) if l.startswith('%chardef end'))
ENT = re.compile(r'^(\S+)(\s+)(\S+)(.*)$')
idx = defaultdict(list)   # key -> [line index]
for i in range(beg + 1, end):
    l = lines[i]
    if not l.strip() or l.startswith('#'): continue
    m = ENT.match(l)
    if m: idx[m.group(1).lower()].append(i)
def cur_list(k):
    out = []
    for i in idx[k]:
        c = ENT.match(lines[i]).group(3)
        if c not in out: out.append(c)
    return out
rows = []
for line in open(rec_in, encoding='utf8'):
    m = re.match(r'^(\S+)\s+(\S+)\s+(\S+)\s+([常次外]+)\s+(\S+)\s', line)
    if m: rows.append(m.groups())
rep = []; changed = 0; merged_chars = []; dropped_simp = []; skipped = []
seen = set()
insertions = []  # (after_line_index, seq, new_line)
for k, cur_s, pr_s, tier, tag in rows:
    if k in seen: continue   # 第二節重複的鍵
    seen.add(k)
    cur = list(cur_s); pr = list(pr_s) if pr_s != '-' else []
    actual = cur_list(k)
    if actual != cur:
        skipped.append((k, cur_s, ''.join(actual))); continue
    T = tag.upper()
    if T in ('A', '保留你的', '保留目前', '傾向保留'): continue
    if T in ('B', '建議採'):
        new = [c for c in pr if c in cur] + [c for c in cur if c not in pr]; how = 'B 採PR順序'
    elif T in ('A+MERGE', 'B+MERGE'):
        base = cur if T.startswith('A') else [c for c in pr if c in cur] + [c for c in cur if c not in pr]
        extra = []
        for c in pr:
            if c in cur: continue
            if gb(c) and not big5(c): dropped_simp.append((k, c)); continue
            extra.append(c); merged_chars.append((k, c, 'Big5' if big5(c) else '擴充'))
        new = base + extra; how = f'{T} 合併 {"".join(extra) or "(無)"}'
    else:
        skipped.append((k, cur_s, f'未知標籤 {tag}')); continue
    if new == cur: continue
    # 既有位置依序填入, 多出的插在最後一行之後
    pos = idx[k]
    for i, c in zip(pos, new):
        m = ENT.match(lines[i]); lines[i] = m.group(1) + m.group(2) + c + m.group(4)
    if len(new) > len(pos):
        last = pos[-1]; m = ENT.match(lines[last])
        for seq, c in enumerate(new[len(pos):]):
            insertions.append((last, seq, m.group(1) + m.group(2) + c + m.group(4)))
    changed += 1
    rep.append(f"{k:5} {''.join(cur):12} -> {''.join(new):14} {how}")
# 由後往前插入, 避免索引位移
# 同一位置的多個字要反序插入，最後插的排最前
for last, seq, nl in sorted(insertions, key=lambda x: (-x[0], -x[1])):
    lines.insert(last + 1, nl)
open(cin_out, 'w', encoding='utf8').write('\n'.join(lines))
with open(report_out, 'w', encoding='utf8') as f:
    f.write(f"套用依據: {rec_in}\n來源: {cin_in}\n輸出: {cin_out}\n\n")
    f.write(f"重排/合併的鍵: {changed}  新增三碼項: {len(merged_chars)}  濾掉簡體: {len(dropped_simp)}  跳過: {len(skipped)}\n\n")
    f.write("== 變更明細 ==\n" + '\n'.join(rep) + '\n')
    f.write("\n== 新增的三碼項 ==\n" + '\n'.join(f"{k:5} {c} [{t}]" for k, c, t in merged_chars) + '\n')
    f.write("\n== 濾掉的簡體字 ==\n" + '\n'.join(f"{k:5} {c}" for k, c in dropped_simp) + '\n')
    f.write("\n== 跳過 (目前順序與表不符或標籤不明) ==\n" + '\n'.join(f"{k:5} 表:{a} 檔:{b}" for k, a, b in skipped) + '\n')
print(open(report_out, encoding='utf8').read())
