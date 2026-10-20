"""Validated document model. Synthetic fixtures only."""
from datetime import date, timedelta
import re

def integer(value, low, high, label):
    if type(value) is not int or not low <= value <= high:
        raise ValueError(f"{label} must be an integer between {low} and {high}.")
    return value

def text(value, label, maximum=120):
    if not isinstance(value, str) or not value.strip() or len(value) > maximum:
        raise ValueError(f"{label} must contain 1–{maximum} characters.")
    return value.strip()

def choice(value, allowed, label):
    if value not in allowed:
        raise ValueError(f"Invalid {label}.")
    return value

def items(raw, key):
    result=raw.get(key)
    if not isinstance(result,list) or len(result)>150:
        raise ValueError(f"{key} must be a list of at most 150 entries.")
    seen=set()
    for item in result:
        if not isinstance(item,dict): raise ValueError("Each entry must be an object.")
        key_id=item.get("id")
        if not isinstance(key_id,str) or not re.fullmatch(r"[a-zA-Z0-9_-]{1,60}",key_id) or key_id in seen:
            raise ValueError("Entry identifiers must be unique and valid.")
        seen.add(key_id)
    return result

def base(raw):
    if not isinstance(raw,dict) or type(raw.get("version")) is not int or raw["version"]!=1:
        raise ValueError("Expected a version 1 document.")
    return {"version":1,"title":text(raw.get("title"),"Title")}
def validate(raw):
    out=base(raw);out["width"]=integer(raw.get("width"),100,1000,"Page width");out["height"]=integer(raw.get("height"),100,1000,"Page height");out["elements"]=[]
    for x in items(raw,"elements"):
        color=x.get("color")
        if not isinstance(color,str) or not re.fullmatch(r"#[0-9a-fA-F]{6}",color):raise ValueError("Use a six-digit hexadecimal color.")
        obj={"id":x["id"],"name":text(x.get("name"),"Layer name"),"kind":choice(x.get("kind"),["text","rectangle","ellipse"],"layer kind"),"x":integer(x.get("x"),0,1000,"X"),"y":integer(x.get("y"),0,1000,"Y"),"width":integer(x.get("width"),5,1000,"Width"),"height":integer(x.get("height"),5,1000,"Height"),"size":integer(x.get("size"),2,40,"Text size"),"text":text(x.get("text") or "—","Layer text",1000),"color":color,"locked":x.get("locked",False)}
        if type(obj["locked"]) is not bool:raise ValueError("Locked must be boolean.")
        if obj["x"]+obj["width"]>out["width"] or obj["y"]+obj["height"]>out["height"]:raise ValueError("A layer extends beyond the page.")
        out["elements"].append(obj)
    return out

def analyze(doc):
    overflow=[e["id"] for e in doc["elements"] if e["kind"]=="text" and (max(map(len,e["text"].splitlines()))*e["size"]*.62>e["width"] or len(e["text"].splitlines())*e["size"]*1.3>e["height"])]
    return {"overflow":overflow,"metrics":{"Layers":len(doc["elements"]),"Locked":sum(e["locked"] for e in doc["elements"]),"Text notices":len(overflow),"Page width mm":doc["width"]}}
