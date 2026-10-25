"""ZIP validation against local vanilla inputs; standard library only."""
import argparse,collections,hashlib,json,re,unicodedata,zipfile
from pathlib import Path
ap=argparse.ArgumentParser()
for opt in ("root","english","japanese"):ap.add_argument("--"+opt,type=Path,required=True)
args=ap.parse_args()
def unique(pairs):
 d={}
 for k,v in pairs:
  if k in d:raise ValueError("Duplicate JSON key: "+k)
  d[k]=v
 return d
def load(path):return json.loads(path.read_text(encoding="utf-8-sig"),object_pairs_hook=unique)
root=args.root;en=load(args.english);ja=load(args.japanese)
release=load(root/"release.json");spans=load(root/"data/annotation-spans.json")
retained=load(root/"data/retained-readings.json")
exceptions=load(root/"data/coverage-exceptions.json")
tech=re.compile(r"%(?:\d+\$)?[-#+ 0,(]*\d*(?:\.\d+)?[A-Za-z%]|%|§[0-9A-FK-ORa-fk-or]|\r\n|\r|\n|https?://[^\s<>\"「」]+")
jp=re.compile(r"[\u3041-\u3096\u30a1-\u30fa\u30fc\u3400-\u9fff]")
pack=root/"dist"/release["archive"]
with zipfile.ZipFile(pack) as z:
 assert z.testzip() is None,"Corrupt ZIP"
 assert len(z.namelist())==5 and set(z.namelist())=={"pack.mcmeta","pack.png","NOTICE.txt","LICENSE.txt","assets/minecraft/lang/ja_jp.json"},"Wrong ZIP layout"
 data=z.read("assets/minecraft/lang/ja_jp.json")
 values=json.loads(data.decode("utf-8"),object_pairs_hook=unique)
 meta=json.loads(z.read("pack.mcmeta").decode("utf-8"),object_pairs_hook=unique)
 assert meta["pack"]["pack_format"]==34
 assert z.read("pack.png").startswith(b"\x89PNG\r\n\x1a\n"),"Invalid pack icon"
 assert z.read("LICENSE.txt")== (root/"LICENSE.txt").read_bytes(),"License mismatch"
 assert data==(root/"pack/assets/minecraft/lang/ja_jp.json").read_bytes()
 assert hashlib.sha256(data).hexdigest()==release["language_sha256"]
 assert len(values)==release["entry_count"]==6506
 assert set(values)==set(release["keys"])==set(spans)
 expected={k for k in en if k in ja and jp.search(ja[k]) and not k.startswith(("language.","translation.test."))}
 assert set(values)==expected,"Incomplete or unexpected Japanese coverage"
 protected_count=0
 for key,value in values.items():
  assert tech.findall(value)==tech.findall(ja[key]),"Changed runtime tokens: "+key
  protected_count+=len(tech.findall(ja[key]))
  actual=[];offset=0
  for at,addition in sorted(spans[key]):
   assert isinstance(at,int) and 0<=at<=len(ja[key])
   assert addition.startswith(" (") and addition.endswith(")")
   assert not re.search(r"[\u3040-\u30ff\u3400-\u9fff々~]",addition),"Unresolved reading: "+key
   assert unicodedata.normalize("NFC",addition)==addition
   actual.append((at+offset,addition));offset+=len(addition)
  restored=value
  for at,addition in reversed(actual):
   assert restored[at:at+len(addition)]==addition,"Incorrect annotation span: "+key
   restored=restored[:at]+restored[at+len(addition):]
  assert restored==ja[key],"Original Japanese altered: "+key
 for key,reading in retained.items():
  assert values[key]==ja[key]+" ("+reading+")","Previous reading changed: "+key
 assert len(retained)==264
 missing=[k for k in en if k not in ja]
 assert missing==exceptions["missing_japanese_keys"]
 skipped={r["key"] for r in exceptions["unchanged_keys"]}
 assert set(en)==set(values)|set(missing)|skipped
 assert not set(values)&skipped
summary={"version":release["version"],"source_keys":len(en),"annotated":len(values),
"preserved_prior_entries":len(retained),"unchanged_keys":len(skipped),"missing_japanese_fallback_keys":len(missing),
"protected_runtime_tokens":protected_count,"categories":dict(collections.Counter(k.split(".")[0] for k in values)),
"zip_bytes":pack.stat().st_size,"zip_sha256":hashlib.sha256(pack.read_bytes()).hexdigest()}
(root/"data/validation-result.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(summary,ensure_ascii=False))
