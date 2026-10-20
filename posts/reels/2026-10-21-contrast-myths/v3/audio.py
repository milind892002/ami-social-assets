# Original warm, upbeat acoustic-pop track (100 BPM), synthesized with numpy. No licensed audio.
import numpy as np, scipy.io.wavfile as w
from scipy.signal import lfilter
sr=44100; B=0.6; DUR=29.0; N=int(sr*DUR)
L=np.zeros(N); R=np.zeros(N); rng=np.random.default_rng(11)
def add(x,t,g=1,pan=0):
    i=int(t*sr); j=min(N,i+len(x))
    if i<N: L[i:j]+=x[:j-i]*g*(1-pan); R[i:j]+=x[:j-i]*g*(1+pan)
mtof=lambda m:440*2**((m-69)/12)
def ks(f,d=1.6,bright=.5):  # Karplus-Strong plucked string
    n=int(sr/f); buf=rng.uniform(-1,1,n); buf=lfilter([bright,1-bright],[1],buf)
    out=np.zeros(int(d*sr)); 
    for i in range(len(out)):
        out[i]=buf[i%n]; buf[i%n]=0.996*0.5*(buf[i%n]+buf[(i+1)%n])
    return out
cache={}
def string(m,d=1.6):
    k=(m,d)
    if k not in cache: cache[k]=ks(mtof(m),d)
    return cache[k]
def strum(notes,t,g=.16,down=True,d=1.2):
    seq=notes if down else notes[::-1]
    for k,m in enumerate(seq): add(string(m,d),t+k*0.012,g*(0.85 if not down else 1),(k/len(seq)-.5)*.5)
def kick():
    t=np.arange(int(.3*sr))/sr; f=48+90*np.exp(-t*25); return np.sin(2*np.pi*np.cumsum(f)/sr)*np.exp(-t*10)
def snap():
    t=np.arange(int(.12*sr))/sr; n=lfilter([1,-1],[1,-.2],rng.standard_normal(len(t)))
    return (n*np.exp(-t*45)+np.sin(2*np.pi*1900*t)*np.exp(-t*80)*.4)*.22
def shaker():
    t=np.arange(int(.07*sr))/sr; n=lfilter([1,-1],[1,0],rng.standard_normal(len(t)))
    return n*np.sin(np.pi*t/.07)*.045
def bass(m,d):
    t=np.arange(int(d*sr))/sr; s=np.sin(2*np.pi*mtof(m)*t)+.25*np.sin(4*np.pi*mtof(m)*t)
    return s*np.minimum(1,t/.01)*np.exp(-t*2.2)*.3
def pad(ms,d):
    t=np.arange(int(d*sr))/sr; s=sum(np.sin(2*np.pi*mtof(m)*t)+.15*np.sin(2*np.pi*mtof(m)*2.003*t) for m in ms)/len(ms)
    env=np.minimum(t/.8,1)*np.minimum((d-t)/.8,1); return s*env*.05
def bell(m):
    t=np.arange(int(1.2*sr))/sr; return (np.sin(2*np.pi*mtof(m)*t)+.3*np.sin(2*np.pi*mtof(m)*3*t)*np.exp(-t*6))*np.exp(-t*3.5)*.07
# C  G  Am  F  (guitar voicings)
prog=[(36,[48,52,55,60,64]),(43,[43,50,55,59,62]),(45,[45,52,57,60,64]),(41,[41,48,53,57,60])]
mel=[76,74,72,74, 74,71,67,71, 72,76,79,76, 77,76,72,69]
nb=int((DUR-1.5)/B)
for b in range(nb):
    t=b*B; bar=b//4; root,ch=prog[bar%4]; beat=b%4
    intro=bar<1
    # strum pattern: D . D U . U D U  (8ths)
    pat=[(0,1),(1,1),(1.5,0),(2.5,0),(3,1),(3.5,0)] if beat==0 else []
    for off,dn in pat: strum(ch,t+off*B,.15 if dn else .1,bool(dn))
    if not intro:
        if beat in (0,2): add(kick(),t,.8)
        if beat in (1,3): add(snap(),t,1)
        for s in range(2): add(shaker(),t+s*B/2,1,.4)
        if beat==0: add(bass(root,B*1.8),t); 
        if beat==2: add(bass(root+7 if root<43 else root-5,B*1.8),t)
    if beat==0: add(pad([m+12 for m in ch[-3:]],4*B+.8),t)
    if bar>=2 and bar%2==0 and beat in (0,1,2,3):
        i=((bar//2)%2)*8+beat*2
        add(bell(mel[i%16]),t,1,.2); add(bell(mel[(i+1)%16]),t+B/2+B/4,1,-.2)
fade=np.clip((DUR-np.arange(N)/sr)/2.0,0,1)
mix=np.stack([L*fade,R*fade],1); mix=mix/np.max(np.abs(mix))*0.9
w.write('audio.wav',sr,(mix*32767).astype(np.int16)); print('ok')
