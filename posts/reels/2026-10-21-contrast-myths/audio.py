# Original synthesized background: soft pad chords + gentle plucks on scene changes.
import numpy as np, scipy.io.wavfile as w
sr=44100; dur=24.0; t=np.arange(int(sr*dur))/sr
def note(f): return 440*2**((f-69)/12)
chords=[[57,60,64],[53,57,60],[55,59,62],[52,55,59]]  # Am F G Em
y=np.zeros_like(t)
for k in range(int(dur/3)+1):
    c=chords[k%4]; a,b=k*3.0,k*3.0+3.4
    m=(t>=a)&(t<b); tt=t[m]-a
    env=np.minimum(tt/0.6,1)*np.minimum((b-t[m])/0.6,1)
    for n in c: y[m]+=0.06*env*(np.sin(2*np.pi*note(n)*tt)+0.3*np.sin(2*np.pi*note(n+12)*tt))
for s in [0,2.8,6.4,10.0,13.4,17.2,21.0]+[3.7,7.3,10.9]:
    m=(t>=s)&(t<s+1.2); tt=t[m]-s
    y[m]+=0.12*np.exp(-tt*5)*np.sin(2*np.pi*note(76)*tt)
y*=np.minimum(1,(dur-t)/1.0)
y=y/np.max(np.abs(y))*0.6
w.write('audio.wav',sr,(y*32767).astype(np.int16))
