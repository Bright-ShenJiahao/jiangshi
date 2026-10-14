import sherpa_onnx, soundfile as sf, numpy as np, sys, json, subprocess, os
K='kokoro-multi-lang-v1_1/'; M='vits-melo-tts-zh_en/'
_k=_m=None
def kok():
    global _k
    if not _k:
        _k=sherpa_onnx.OfflineTts(sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(kokoro=sherpa_onnx.OfflineTtsKokoroModelConfig(
          model=K+'model.onnx',voices=K+'voices.bin',tokens=K+'tokens.txt',data_dir=K+'espeak-ng-data',dict_dir=K+'dict',lexicon=K+'lexicon-zh.txt,'+K+'lexicon-us-en.txt'),num_threads=2),
          rule_fsts=K+'date-zh.fst,'+K+'number-zh.fst,'+K+'phone-zh.fst'))
    return _k
def melo():
    global _m
    if not _m:
        _m=sherpa_onnx.OfflineTts(sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(vits=sherpa_onnx.OfflineTtsVitsModelConfig(
          model=M+'model.onnx',lexicon=M+'lexicon.txt',tokens=M+'tokens.txt',dict_dir=M+'dict'),num_threads=2),
          rule_fsts=M+'date.fst,'+M+'phone.fst,'+M+'number.fst,'+M+'new_heteronym.fst'))
    return _m
def say(text, out, model='k', sid=0, speed=1.0, pitch=1.0, echo=False, vol=1.0):
    t = kok() if model=='k' else melo()
    a=t.generate(text,sid=sid,speed=speed); raw=out+'.raw.wav'
    sf.write(raw,np.array(a.samples),a.sample_rate)
    sr=a.sample_rate
    af=[]
    if pitch!=1.0: af+= [f'asetrate={int(sr*pitch)}',f'aresample={sr}',f'atempo={1/pitch:.4f}']
    if echo: af.append('aecho=0.8:0.5:60|110:0.18|0.10')
    af+=[f'volume={vol}','loudnorm=I=-16:TP=-1.5:LRA=11','silenceremove=start_periods=1:start_threshold=-50dB']
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i',raw,'-af',','.join(af),'-ac','1','-ar','24000','-b:a','40k',out],check=True)
    os.remove(raw)
if __name__=='__main__':
    for j in json.load(open(sys.argv[1])):
        say(**j); print(j['out'], flush=True)
