import argparse,hashlib,json
from pathlib import PurePosixPath
ALLOWED={"text/plain","application/json","text/markdown"}
def intake(files,max_files=100,max_bytes=10_000_000):
 errors=[]; seen=set(); clean=[]
 if not isinstance(files,list) or len(files)>max_files: return {"accepted":False,"errors":["file_count"],"files":[]}
 for item in files:
  name=item.get("name") if isinstance(item,dict) else None; size=item.get("size") if isinstance(item,dict) else None; digest=item.get("sha256") if isinstance(item,dict) else None; media=item.get("media_type") if isinstance(item,dict) else None
  if not isinstance(name,str) or PurePosixPath(name).is_absolute() or ".." in PurePosixPath(name).parts or name in seen: errors.append("invalid_or_duplicate_name"); continue
  seen.add(name)
  if not isinstance(size,int) or isinstance(size,bool) or size<0 or size>max_bytes: errors.append(f"size:{name}")
  if not isinstance(digest,str) or len(digest)!=64 or any(c not in "0123456789abcdef" for c in digest): errors.append(f"sha:{name}")
  if media not in ALLOWED: errors.append(f"media:{name}")
  clean.append({"name":name,"size":size,"sha256":digest,"media_type":media})
 clean.sort(key=lambda x:x["name"]); manifest=hashlib.sha256(json.dumps(clean,sort_keys=True,separators=(",",":")).encode()).hexdigest()
 return {"accepted":not errors,"errors":errors,"files":clean,"manifest_sha256":manifest}
def probe():
 g=intake([{"name":"a.txt","size":1,"sha256":"a"*64,"media_type":"text/plain"}]); b=intake([{"name":"../x","size":1,"sha256":"a"*64,"media_type":"text/plain"}]); return {"ok":g["accepted"] and not b["accepted"],"counter_proof":not b["accepted"]}
def main(argv=None):
 p=argparse.ArgumentParser(); p.add_argument("command",choices=("intake","probe")); p.add_argument("--input"); a=p.parse_args(argv); out=probe() if a.command=="probe" else intake(json.load(open(a.input))["files"]); print(json.dumps(out,sort_keys=True)); return 0 if out.get("ok",out.get("accepted")) else 2
