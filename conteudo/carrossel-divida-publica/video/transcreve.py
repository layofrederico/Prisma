import json, sys
from faster_whisper import WhisperModel
m = WhisperModel("medium", device="cpu", compute_type="int8")
segs, info = m.transcribe(sys.argv[1], language="pt", word_timestamps=True, vad_filter=False,
    initial_prompt="Hum, é, ahn... Hoje, cada brasileiro deve cinquenta e um mil reais.", condition_on_previous_text=False)
out=[]
for s in segs:
    for w in s.words:
        out.append({"w":w.word,"s":round(w.start,2),"e":round(w.end,2),"p":round(w.probability,2)})
json.dump(out, open(sys.argv[2],"w"), ensure_ascii=False, indent=0)
for w in out: print("%6.2f %6.2f %4.2f %s"%(w["s"],w["e"],w["p"],w["w"]))
