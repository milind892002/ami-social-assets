# Original upbeat track, 128 BPM, synthesized with numpy (no licensed audio). SFX synced to the animation.
import numpy as np, scipy.io.wavfile as w
from scipy.signal import lfilter
sr=44100; B=60/128; DUR=25.0
N=int(sr*DUR); L=np.zeros(N); Rr=np.zeros(N)
rng=np.random.default_rng(3)
def add(sig,t0,g=1.0,pan=0.0):
    i=int(t0*sr); j=min(N,i+len(sig))
    if i>=N: return
    L[i:j]+=sig[:j-i]*g*(1-pan); Rr[i:j]+=sig[:j-i]*g*(1+pan)
def mtof(m): return 440*2**((m-69)/12)
def kick():
    t=np.arange(int(.35*sr))/sr; f=50+120*np.exp(-t*30)
    return np.sin(2*np.pi*np.cumsum(f)/sr)*np.exp(-t*9)
def clap():
    t=np.arange(int(.2*sr))/sr; n=rng.standard_normal(len(t))
    n=lfilter([1,-1],[1,-.6],n); env=np.exp(-t*25)+0.5*np.exp(-((t-.012)%0.011)*200)*(t<.035)
    return n*env*0.35
def hat(open_=False):
    t=np.arange(int((.18 if open_ else .05)*sr))/sr; n=rng.standard_normal(len(t))
    n=lfilter([1,-1],[1,0],n); return n*np.exp(-t*(18 if open_ else 70))*0.12
def saw(f,d,det=0.004):
    t=np.arange(int(d*sr))/sr; s=0
    for dd in (-det,0,det): s=s+2*((t*f*(1+dd))%1)-1
    return s/3
def lp(x,a): return lfilter([1-a],[1,-a],x)
def pluck(m,d=.22):
    t=np.arange(int(d*sr))/sr; s=saw(mtof(m),d)*np.exp(-t*14); return lp(s,.55)*0.22
def stab(ms,d=.3):
    t=np.arange(int(d*sr))/sr; s=sum(saw(mtof(m),d) for m in ms)/len(ms)
    return lp(s,.7)*np.exp(-t*7)*0.28
def bass(m,d):
    t=np.arange(int(d*sr))/sr; s=np.sign(np.sin(2*np.pi*mtof(m)*t))*0.5+np.sin(2*np.pi*mtof(m)*t)
    return lp(s,.88)*np.minimum(1,t/.005)*np.exp(-t*3)*0.35
def boom():
    t=np.arange(int(.9*sr))/sr; f=40+180*np.exp(-t*12)
    s=np.sin(2*np.pi*np.cumsum(f)/sr)*np.exp(-t*4)
    n=lfilter([1,-1],[1,-.3],rng.standard_normal(len(t)))*np.exp(-t*18)*.4
    return (s+n)*0.8
def tick(hi=False):
    t=np.arange(int(.09*sr))/sr; return np.sin(2*np.pi*(1800 if hi else 1300)*t)*np.exp(-t*60)*0.35
def sparkle():
    out=np.zeros(int(1.0*sr))
    for k,m in enumerate([84,88,91,96,100]):
        s=np.sin(2*np.pi*mtof(m)*np.arange(int(.4*sr))/sr)*np.exp(-np.arange(int(.4*sr))/sr*9)*0.12
        i=int(k*.06*sr); out[i:i+len(s)]+=s
    return out
def whoosh(d=.45):
    t=np.arange(int(d*sr))/sr; n=rng.standard_normal(len(t)); a=0.6+0.35*(t/d)
    y=np.zeros_like(n); prev=0
    for i in range(len(n)): prev=a[i]*prev+(1-a[i])*n[i]; y[i]=prev
    return y*np.sin(np.pi*t/d)**2*1.2
# progression C G Am F (2 beats? no: 1 bar each = 4 beats)
prog=[(48,[60,64,67]),(43,[59,62,67]),(45,[60,64,69]),(41,[60,65,69])]
arp=[72,76,79,76,74,79,83,79,72,76,81,76,72,77,81,77]
HOOK=8*B; RL=12*B; END0=HOOK+3*RL
nbeats=int(DUR/B)
for b in range(nbeats):
    t=b*B; bar=b//4; root,ch=prog[bar%4]
    intro=b<4
    if not intro or b%2==0: add(kick(),t,0.9)
    if b%2==1 and not intro: add(clap(),t,1.0)
    add(hat(),t+B/2,1.0,0.3); 
    if not intro: add(hat(),t+B/4,0.6,-0.3); add(hat(),t+3*B/4,0.6,-0.3)
    add(bass(root,B*0.45),t,1.0); add(bass(root+12 if b%2 else root,B*0.4),t+B/2,0.8)
    if b%2==0: add(stab(ch,.25),t+B/2,1.0)  # offbeat stabs
    for s in range(2):  # 8th-note pluck arp
        add(pluck(arp[(b*2+s)%16]),t+s*B/2,0.9,0.4 if s else -0.4)
# SFX
for k,tt in enumerate([0,B,2*B]): add(boom(),tt,0.7)
add(sparkle(),3*B,0.8)
for r in range(3):
    s=HOOK+r*RL
    add(whoosh(),s-0.3,0.5); add(boom(),s+0.05,0.5)
    for k in range(3): add(tick(k==2),s+(4+k)*B,1.0)
    add(boom(),s+8*B,1.0); add(sparkle(),s+8*B+0.05,1.0)
add(whoosh(),END0-0.3,0.5); add(boom(),END0,0.6); add(sparkle(),END0+B,0.7); add(boom(),END0+4*B,0.6)
# sidechain-ish duck on kicks
duck=np.ones(N)
for b in range(nbeats):
    i=int(b*B*sr); n=int(.18*sr); duck[i:i+n]=np.minimum(duck[i:i+n],0.55+0.45*np.linspace(0,1,n)**.7)
# fade end
fade=np.clip((DUR-np.arange(N)/sr)/1.2,0,1)
mix=np.stack([L*duck*fade,Rr*duck*fade],1)
mix=np.tanh(mix*1.6)/np.tanh(1.6)
mix=mix/np.max(np.abs(mix))*0.89
w.write('audio.wav',sr,(mix*32767).astype(np.int16))
print('ok')
