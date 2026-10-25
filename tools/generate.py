"""Build-time Japanese readings. Runtime pack contains only static JSON.
Requires SudachiPy==0.6.10 and SudachiDict-core==20250129.
"""
import argparse, collections, json, re, sys, unicodedata, zipfile
from pathlib import Path
ap=argparse.ArgumentParser()
ap.add_argument("--english",type=Path,required=True)
ap.add_argument("--japanese",type=Path,required=True)
ap.add_argument("--deps",type=Path,required=True)
ap.add_argument("--out",type=Path,required=True)
ap.add_argument("--previous",type=Path)
ap.add_argument("--retained",type=Path)
ap.add_argument("--overrides",type=Path,required=True)
args=ap.parse_args()
sys.path.insert(0,str(args.deps.resolve()))
from sudachipy import dictionary, tokenizer
tok=dictionary.Dictionary().create()
en=json.loads(args.english.read_text(encoding="utf-8-sig"))
ja=json.loads(args.japanese.read_text(encoding="utf-8-sig"))
if args.retained:
    prior={key:ja[key]+" ("+reading+")" for key,reading in json.loads(args.retained.read_text(encoding="utf-8")).items()}
elif args.previous:
    with zipfile.ZipFile(args.previous) as z:
        prior=json.loads(z.read("assets/minecraft/lang/ja_jp.json"))
else:
    ap.error("Supply --retained or --previous.")
overrides=json.loads(args.overrides.read_text(encoding="utf-8"))
phrases=dict(overrides["phrases"])
for key,value in prior.items():
    original=ja[key]
    assert value.startswith(original+" (") and value.endswith(")")
    phrases[original]=value[len(original)+2:-1]
whole_phrases=dict(phrases)
phrases={s:r for s,r in phrases.items() if len(s)>1}
phrase_re=re.compile("|".join(re.escape(s) for s in sorted(phrases,key=len,reverse=True)))
JP=re.compile(r"[\u3041-\u3096\u30a1-\u30fa\u30fc\u3400-\u9fff]")
KANJI=re.compile(r"[\u3400-\u9fff]")
PROTECT=re.compile(r"(%(?:\d+\$)?[-#+ 0,(]*\d*(?:\.\d+)?[A-Za-z%]|%|§[0-9A-FK-ORa-fk-or]|\r\n|\r|\n|https?://[^\s<>\"「」]+|[「」『』（）()\[\]【】])")
TECH_PROTECT=re.compile(r"(%(?:\d+\$)?[-#+ 0,(]*\d*(?:\.\d+)?[A-Za-z%]|%|§[0-9A-FK-ORa-fk-or]|\r\n|\r|\n|https?://[^\s<>\"「」]+)")
# Kana-to-Hepburn conversion; dictionary output is kana, not an English translation.
kana={}
for chars,rom in [
("アイウエオ","a i u e o"),("カキクケコ","ka ki ku ke ko"),
("ガギグゲゴ","ga gi gu ge go"),("サシスセソ","sa shi su se so"),
("ザジズゼゾ","za ji zu ze zo"),("タチツテト","ta chi tsu te to"),
("ダヂヅデド","da ji zu de do"),("ナニヌネノ","na ni nu ne no"),
("ハヒフヘホ","ha hi fu he ho"),("バビブベボ","ba bi bu be bo"),
("パピプペポ","pa pi pu pe po"),("マミムメモ","ma mi mu me mo"),
("ヤユヨ","ya yu yo"),("ラリルレロ","ra ri ru re ro"),
("ワヰヱヲン","wa i e o n"),("ァィゥェォ","a i u e o"),
("ャュョヮヵヶヴ","ya yu yo wa ka ke vu")]:
    kana.update(zip(chars,rom.split()))
for k,stem in {"キ":"ky","ギ":"gy","シ":"sh","ジ":"j","チ":"ch","ヂ":"j",
"ニ":"ny","ヒ":"hy","ビ":"by","ピ":"py","ミ":"my","リ":"ry"}.items():
    for small,v in zip("ャュョ","auo"):kana[k+small]=stem+v
kana.update(dict(zip(
"イェ ウィ ウェ ウォ ヴァ ヴィ ヴェ ヴォ ヴュ シェ ジェ チェ ティ ディ トゥ ドゥ テュ デュ ツァ ツィ ツェ ツォ ファ フィ フェ フォ フュ クァ クィ クェ クォ グァ グィ グェ グォ".split(),
"ye wi we wo va vi ve vo vyu she je che ti di tu du tyu dyu tsa tsi tse tso fa fi fe fo fyu kwa kwi kwe kwo gwa gwi gwe gwo".split())))
vowels="aeiou"
longs=dict(zip(vowels,"āēīōū"))
unknown=collections.Counter()
tokens=collections.Counter()
def roman_kana(s,pos):
    s=unicodedata.normalize("NFKC",s)
    s="".join(chr(ord(c)+96) if "\u3041"<=c<="\u3096" else c for c in s)
    out=[];i=0;geminate=False
    while i<len(s):
        c=s[i]
        if c=="ッ":
            if i==len(s)-1:out.append("~")
            geminate=True;i+=1;continue
        if c=="ー":
            if out:
                last=out[-1]
                for n in range(len(last)-1,-1,-1):
                    if last[n] in vowels:
                        out[-1]=last[:n]+longs[last[n]]+last[n+1:];break
            i+=1;continue
        unit=s[i:i+2] if s[i:i+2] in kana else c
        ro=kana.get(unit,unit.lower())
        if c=="ン" and i+1<len(s):
            nextro=kana.get(s[i+1:i+3],kana.get(s[i+1],""))
            if nextro[:1] in list(vowels)+["y"]:ro="n'"
        if geminate and ro and ro[0].isascii() and ro[0].isalpha():
            ro=("t" if ro.startswith("ch") else ro[0])+ro
        geminate=False
        out.append(ro);i+=len(unit)
    r="".join(out)
    # Common noun long-vowel spelling; leave verb vowel sequences intact (omou).
    if pos in {"名詞","接尾辞","形状詞","形容詞"}:
        r=r.replace("ou","ō").replace("oo","ō").replace("uu","ū").replace("aa","ā")
    return r
def plain_reading(s,key):
    parts=[]
    for m in tok.tokenize(s,tokenizer.Tokenizer.SplitMode.C):
        surface=m.surface();p=m.part_of_speech();rd=m.reading_form()
        if not JP.search(surface):
            r=" " if surface=="・" else surface.lower()
        elif surface in overrides["tokens"] and p[0]!="接尾辞":
            r=overrides["tokens"][surface]
        elif p[0]=="助詞" and surface in {"は","へ","を"}:
            r={"は":"wa","へ":"e","を":"o"}[surface]
        else:
            r=roman_kana(rd,p[0])
        if JP.search(r):unknown[(surface,rd,r,key)]+=1
        tokens[(surface,rd,r,p[0])]+=1
        # Inflectional endings form words with the preceding stem.
        attach=p[0] in {"助動詞","接尾辞"} or (surface in {"て","で"} and p[1]=="接続助詞")
        if attach and parts and not parts[-1].isspace():parts[-1]+=r
        else:parts.append(r)
    r=" ".join(parts)
    r=re.sub(r"~\s*(ch|[a-z])",lambda m: ("t" if m[1]=="ch" else m[1])+m[1],r)
    r=r.replace("oo","ō")
    r=re.sub(r"\s+"," ",r).strip()
    r=r.translate(str.maketrans({"、":",","。":".","！":"!","？":"?","：":":","；":";","（":"(","）":")","「":chr(34),"」":chr(34),"『":chr(34),"』":chr(34)}))
    r=re.sub(r"\s+([,.!?;:、。！？：；）』」])",r"\1",r)
    r=re.sub(r"([（『「])\s+",r"\1",r)
    return r
def read(s,key):
    if s in whole_phrases:return whole_phrases[s]
    out=[];start=0
    for m in phrase_re.finditer(s):
        if m.start()>start:out.append(plain_reading(s[start:m.start()],key))
        out.append(phrases[m.group()]);start=m.end()
    if start<len(s):out.append(plain_reading(s[start:],key))
    return re.sub(r"\s+"," "," ".join(out)).strip()
def annotate_chunk(s,key):
    if not JP.search(s):return s,[]
    # Leave boundary punctuation outside the annotation, in its original position.
    hits=list(JP.finditer(s))
    a,b=hits[0].start(),hits[-1].end()
    prefix=s[:a]
    alnum=re.search(r"[A-Za-z0-9]",prefix)
    if alnum:a=alnum.start()
    while b<len(s) and s[b].isascii() and s[b].isalnum():b+=1
    # Include leading/trailing ASCII words/numbers within ordinary phrases, but
    # retain surrounding punctuation. Japanese detection controls whether to annotate.
    middle=s[a:b]
    r=read(middle,key)
    insertion=" ("+r+")"
    return s[:b]+insertion+s[b:],[(b,insertion)]
out={};audit=[];skips=[];missing=[]
for key in en:
    if key not in ja:missing.append(key);continue
    original=ja[key]
    if key.startswith(("language.","translation.test.")):
        skips.append({"key":key,"reason":"technical metadata or translation test"});continue
    if not JP.search(original):
        skips.append({"key":key,"reason":"no Japanese script"});continue
    if key in prior:
        value=prior[key]
        insertions=[(len(original),value[len(original):])]
    else:
        parts=PROTECT.split(original);value="";insertions=[];offset=0
        for part in parts:
            if PROTECT.fullmatch(part or "\0"):new=part;adds=[]
            else:new,adds=annotate_chunk(part,key)
            insertions.extend((offset+at,text) for at,text in adds)
            value+=new;offset+=len(part)
    assert value!=original,key
    # Reconstruct the original exclusively by removing recorded additions.
    rebuilt=original
    for at,addition in sorted(insertions,reverse=True):rebuilt=rebuilt[:at]+addition+rebuilt[at:]
    assert rebuilt==value,key
    assert TECH_PROTECT.findall(original)==TECH_PROTECT.findall(value),key
    out[key]=value
    audit.append({"key":key,"original":original,"value":value,"insertions":insertions,
                  "method":"retained" if key in prior else "dictionary-with-overrides"})
args.out.mkdir(parents=True,exist_ok=True)
def write(name,data): (args.out/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
write("ja_jp.json",out);write("audit.json",audit);write("skipped.json",skips);write("missing.json",missing)
write("unknown.json",[dict(surface=a,kana=b,reading=c,key=d,count=n) for (a,b,c,d),n in unknown.items()])
write("tokens.json",[dict(surface=a,kana=b,reading=c,pos=d,count=n) for (a,b,c,d),n in tokens.most_common()])
print(json.dumps({"annotated":len(out),"retained":len(prior),"skipped":len(skips),"missing_ja":len(missing),"unresolved_readings":len(unknown)},ensure_ascii=False))
