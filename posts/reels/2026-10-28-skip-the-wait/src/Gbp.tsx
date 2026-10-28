import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {BODY, C, Check, HEAD, useFonts} from './brand';

export const Gbp: React.FC = () => {
  useFonts();
  const item = (t: string) => (
    <div style={{display: 'flex', alignItems: 'center', gap: 20, marginBottom: 18}}>
      <Check size={46} />
      <span style={{fontFamily: HEAD, fontWeight: 700, fontSize: 36, color: C.white}}>{t}</span>
    </div>
  );
  return (
    <AbsoluteFill style={{background: C.navy, flexDirection: 'row'}}>
      <div style={{width: 470, height: 900, overflow: 'hidden', position: 'relative'}}>
        <Img src={staticFile('waiting-2.jpg')} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
        <div style={{position: 'absolute', inset: 0, background: `linear-gradient(90deg, transparent 55%, ${C.navy} 100%)`}} />
      </div>
      <div style={{flex: 1, padding: '70px 64px 60px 40px', display: 'flex', flexDirection: 'column', justifyContent: 'center'}}>
        <div style={{fontFamily: BODY, fontWeight: 700, fontSize: 22, letterSpacing: 4, color: C.light, marginBottom: 18}}>SELF-PAY AT AMI</div>
        <div style={{fontFamily: HEAD, fontWeight: 800, fontSize: 66, lineHeight: 1.04, letterSpacing: -1.5, color: C.white}}>
          Waiting on insurance approval?
        </div>
        <div style={{fontFamily: HEAD, fontWeight: 800, fontSize: 66, lineHeight: 1.04, color: C.light, marginBottom: 40}}>Skip the wait.</div>
        {item('No referral needed')}
        {item('No prior authorization')}
        {item('MRI $295, reading included')}
        <div style={{marginTop: 30, alignSelf: 'flex-start', background: C.light, color: C.navy, fontFamily: HEAD, fontWeight: 800, fontSize: 30, borderRadius: 999, padding: '16px 34px'}}>
          Book at advancedimg.com
        </div>
      </div>
    </AbsoluteFill>
  );
};
