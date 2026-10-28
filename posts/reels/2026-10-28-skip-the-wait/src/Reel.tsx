import React from 'react';
import {
  AbsoluteFill,
  Img,
  Easing,
  Sequence,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import {BODY, C, Check, HEAD, useFonts} from './brand';

// Scene timing (30 fps)
const S = {
  hook: [0, 100],
  wait: [100, 230],
  turn: [230, 305],
  perks: [305, 425],
  price: [425, 530],
  end: [530, 640],
} as const;
export const REEL_FRAMES = 640;

// Reels safe area: keep text clear of the top bar, bottom caption and right-side buttons.
const PAD_L = 96;
const PAD_R = 150;

const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;

/** Fade + lift in, fade out at the end of a scene of `len` frames. */
const useInOut = (len: number, outFrames = 10) => {
  const f = useCurrentFrame();
  const inP = interpolate(f, [0, 10], [0, 1], {...clamp, easing: Easing.out(Easing.cubic)});
  const out = interpolate(f, [len - outFrames, len], [1, 0], clamp);
  return {opacity: Math.min(inP, out), f};
};

const Background: React.FC = () => {
  const f = useCurrentFrame();
  const a = Math.sin(f / 60) * 120;
  const b = Math.cos(f / 75) * 140;
  return (
    <AbsoluteFill style={{background: C.navy, overflow: 'hidden'}}>
      <div
        style={{
          position: 'absolute', width: 1300, height: 1300, borderRadius: '50%',
          left: -380 + a, top: -300 + b,
          background: `radial-gradient(circle, ${C.blue}66 0%, transparent 62%)`,
        }}
      />
      <div
        style={{
          position: 'absolute', width: 1200, height: 1200, borderRadius: '50%',
          right: -420 - a, bottom: -260 - b,
          background: `radial-gradient(circle, ${C.deep} 0%, transparent 65%)`,
        }}
      />
    </AbsoluteFill>
  );
};

// ---------- Scene 1: hook ----------
const HookWord: React.FC<{text: string; delay: number; color?: string}> = ({text, delay, color = C.white}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const s = spring({frame: f - delay, fps, config: {damping: 14, stiffness: 160}});
  return (
    <div style={{overflow: 'hidden', paddingBottom: 8}}>
      <div
        style={{
          transform: `translateY(${(1 - s) * 110}%)`,
          fontFamily: HEAD, fontWeight: 800, fontSize: 132, lineHeight: 1.02,
          letterSpacing: -3, color,
        }}
      >
        {text}
      </div>
    </div>
  );
};

const Hook: React.FC = () => {
  const len = S.hook[1] - S.hook[0];
  const {opacity, f} = useInOut(len);
  const eyebrow = interpolate(f, [0, 12], [0, 1], clamp);
  return (
    <AbsoluteFill style={{opacity, justifyContent: 'center', paddingLeft: PAD_L, paddingRight: PAD_R}}>
      <div style={{opacity: eyebrow, fontFamily: BODY, fontWeight: 700, fontSize: 34, letterSpacing: 5, color: C.light, marginBottom: 36}}>
        FAQ · PRIOR AUTHORIZATION
      </div>
      <HookWord text="Waiting on" delay={4} />
      <HookWord text="insurance to" delay={10} />
      <HookWord text="approve" delay={16} />
      <HookWord text="your scan?" delay={22} color={C.light} />
    </AbsoluteFill>
  );
};

// ---------- Scene 2: the wait ----------
const Spinner: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <svg width="56" height="56" viewBox="0 0 50 50" style={{transform: `rotate(${f * 12}deg)`}}>
      <circle cx="25" cy="25" r="20" stroke={`${C.amber}44`} strokeWidth="6" fill="none" />
      <path d="M25 5 a20 20 0 0 1 20 20" stroke={C.amber} strokeWidth="6" fill="none" strokeLinecap="round" />
    </svg>
  );
};

const Wait: React.FC = () => {
  const len = S.wait[1] - S.wait[0];
  const {opacity, f} = useInOut(len);
  const {fps} = useVideoConfig();
  const pop = spring({frame: f, fps, config: {damping: 15}});
  const day = Math.min(14, 1 + Math.floor(Math.max(0, f - 22) / 6));
  const flip = ((f - 22) % 6) / 6;
  const pulse = 0.55 + 0.45 * Math.abs(Math.sin(f / 7));
  const status = f < 40 ? 'Submitted' : 'In review';
  const dots = '.'.repeat(1 + (Math.floor(f / 8) % 3));
  const caption = interpolate(f, [30, 45], [0, 1], clamp);

  const row = (label: string, right: React.ReactNode) => (
    <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '30px 0', borderTop: `2px solid ${C.white}14`}}>
      <span style={{fontFamily: BODY, fontSize: 38, fontWeight: 600, color: `${C.white}cc`}}>{label}</span>
      {right}
    </div>
  );

  return (
    <AbsoluteFill style={{opacity, justifyContent: 'center', paddingLeft: PAD_L, paddingRight: PAD_R}}>
      <div
        style={{
          transform: `scale(${0.9 + pop * 0.1}) translateY(${(1 - pop) * 60}px)`,
          background: `${C.deep}ee`, borderRadius: 40, padding: '44px 52px',
          border: `2px solid ${C.white}1f`, boxShadow: '0 40px 80px #00000055',
        }}
      >
        <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 18}}>
          <div style={{fontFamily: HEAD, fontWeight: 800, fontSize: 52, color: C.white}}>Your scan request</div>
          <Spinner />
        </div>
        {row("Doctor's order", <span style={{fontFamily: BODY, fontWeight: 700, fontSize: 36, color: C.green}}>Sent ✓</span>)}
        {row(
          'Prior authorization',
          <span
            style={{
              fontFamily: BODY, fontWeight: 700, fontSize: 34, color: C.navy,
              background: C.amber, borderRadius: 999, padding: '10px 26px', opacity: pulse,
            }}
          >
            {status}
          </span>,
        )}
        {row(
          'Scan date',
          <span style={{fontFamily: BODY, fontWeight: 700, fontSize: 36, color: `${C.white}88`}}>Waiting{dots}</span>,
        )}
        <div style={{display: 'flex', alignItems: 'center', gap: 28, marginTop: 26}}>
          <div style={{width: 150, borderRadius: 22, overflow: 'hidden', textAlign: 'center', background: C.white}}>
            <div style={{background: '#E25555', color: C.white, fontFamily: BODY, fontWeight: 800, fontSize: 24, padding: '6px 0', letterSpacing: 3}}>DAY</div>
            <div
              style={{
                fontFamily: HEAD, fontWeight: 800, fontSize: 84, color: C.navy, padding: '4px 0 10px',
                transform: f > 22 && day < 14 ? `rotateX(${flip * 25}deg)` : undefined,
              }}
            >
              {day}
            </div>
          </div>
          <div style={{fontFamily: BODY, fontSize: 36, lineHeight: 1.35, color: `${C.white}cc`, opacity: caption}}>
            Some plans review a scan before they&apos;ll cover it.
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

// ---------- Scene 3: the turn ----------
const Turn: React.FC = () => {
  const len = S.turn[1] - S.turn[0];
  const {opacity, f} = useInOut(len, 8);
  const {fps} = useVideoConfig();
  const a = spring({frame: f, fps, config: {damping: 12, stiffness: 180}});
  const b = spring({frame: f - 10, fps, config: {damping: 12, stiffness: 180}});
  const line = interpolate(f, [16, 34], [0, 1], {...clamp, easing: Easing.out(Easing.cubic)});
  return (
    <AbsoluteFill style={{opacity, justifyContent: 'center', paddingLeft: PAD_L, paddingRight: PAD_R}}>
      <div style={{fontFamily: HEAD, fontWeight: 800, fontSize: 120, color: C.white, transform: `translateX(${(1 - a) * -200}px)`, opacity: a}}>
        Or&hellip;
      </div>
      <div style={{fontFamily: HEAD, fontWeight: 800, fontSize: 150, lineHeight: 1, letterSpacing: -4, color: C.light, transform: `scale(${0.6 + b * 0.4})`, transformOrigin: 'left center', opacity: b}}>
        skip the wait.
      </div>
      <div style={{height: 14, borderRadius: 7, background: C.light, width: `${line * 78}%`, marginTop: 30}} />
    </AbsoluteFill>
  );
};

// ---------- Scene 4: self-pay perks ----------
const Perk: React.FC<{text: string; delay: number}> = ({text, delay}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const s = spring({frame: f - delay, fps, config: {damping: 13, stiffness: 150}});
  const tick = spring({frame: f - delay - 6, fps, config: {damping: 9, stiffness: 220}});
  return (
    <div
      style={{
        display: 'flex', alignItems: 'center', gap: 34, opacity: s,
        transform: `translateX(${(1 - s) * 140}px)`,
        background: `${C.white}10`, border: `2px solid ${C.white}22`, borderRadius: 30,
        padding: '34px 38px', marginBottom: 28,
      }}
    >
      <div style={{transform: `scale(${tick})`}}>
        <Check size={78} />
      </div>
      <div style={{fontFamily: HEAD, fontWeight: 800, fontSize: 58, lineHeight: 1.08, color: C.white}}>{text}</div>
    </div>
  );
};

const Perks: React.FC = () => {
  const len = S.perks[1] - S.perks[0];
  const {opacity} = useInOut(len);
  return (
    <AbsoluteFill style={{opacity, justifyContent: 'center', paddingLeft: PAD_L, paddingRight: PAD_R}}>
      <div style={{fontFamily: BODY, fontWeight: 700, fontSize: 34, letterSpacing: 5, color: C.light, marginBottom: 20}}>SELF-PAY AT AMI</div>
      <div style={{fontFamily: HEAD, fontWeight: 800, fontSize: 92, lineHeight: 1.02, color: C.white, marginBottom: 54}}>
        No waiting on approvals.
      </div>
      <Perk text="No referral needed" delay={10} />
      <Perk text="No prior authorization" delay={24} />
      <Perk text="Same-day scans often available" delay={38} />
    </AbsoluteFill>
  );
};

// ---------- Scene 5: price ----------
const Price: React.FC = () => {
  const len = S.price[1] - S.price[0];
  const {opacity, f} = useInOut(len);
  const {fps} = useVideoConfig();
  const count = Math.round(interpolate(f, [6, 40], [0, 295], {...clamp, easing: Easing.out(Easing.cubic)}));
  const land = spring({frame: f - 38, fps, config: {damping: 8, stiffness: 200}});
  const sub = interpolate(f, [42, 54], [0, 1], clamp);
  const zoom = interpolate(f, [0, len], [1.05, 1.15]);
  return (
    <AbsoluteFill style={{opacity}}>
      <AbsoluteFill style={{overflow: 'hidden'}}>
        <Img src={staticFile('waiting-2.jpg')} style={{width: '100%', height: '100%', objectFit: 'cover', transform: `scale(${zoom})`}} />
        <AbsoluteFill style={{background: `linear-gradient(180deg, ${C.navy}cc 0%, ${C.navy}e6 45%, ${C.navy} 100%)`}} />
      </AbsoluteFill>
      <AbsoluteFill style={{justifyContent: 'center', paddingLeft: PAD_L, paddingRight: PAD_R}}>
        <div style={{fontFamily: BODY, fontWeight: 700, fontSize: 34, letterSpacing: 5, color: C.light}}>SELF-PAY MRI</div>
        <div style={{fontFamily: HEAD, fontWeight: 800, fontSize: 300, lineHeight: 1, letterSpacing: -10, color: C.white, transform: `scale(${1 + land * 0.06 - 0.06 * (f > 38 ? 0 : 1) * 0})`}}>
          ${count}
        </div>
        <div style={{opacity: sub, transform: `translateY(${(1 - sub) * 20}px)`}}>
          <div style={{fontFamily: HEAD, fontWeight: 700, fontSize: 52, color: C.white, marginTop: 10}}>Radiologist&apos;s reading included.</div>
          <div style={{fontFamily: HEAD, fontWeight: 700, fontSize: 52, color: C.light, marginTop: 14}}>HSA/FSA cards accepted.</div>
        </div>
        <div style={{position: 'absolute', bottom: 430, left: PAD_L, fontFamily: BODY, fontSize: 26, color: `${C.white}99`, opacity: sub}}>
          Our Seminole office
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// ---------- Scene 6: end card ----------
const End: React.FC = () => {
  const len = S.end[1] - S.end[0];
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const inP = interpolate(f, [0, 10], [0, 1], clamp);
  const logo = spring({frame: f, fps, config: {damping: 14}});
  const btn = spring({frame: f - 8, fps, config: {damping: 11, stiffness: 160}});
  const pulse = 1 + 0.035 * Math.sin(Math.max(0, f - 25) / 5);
  const rest = interpolate(f, [18, 30], [0, 1], clamp);
  void len;
  return (
    <AbsoluteFill style={{opacity: inP, justifyContent: 'center', paddingLeft: PAD_L, paddingRight: PAD_R}}>
      <Img src={staticFile('lockup_pill.png')} style={{width: 470, transform: `scale(${logo})`, transformOrigin: 'left center', marginBottom: 60}} />
      <div style={{fontFamily: HEAD, fontWeight: 800, fontSize: 112, lineHeight: 1.02, letterSpacing: -3, color: C.white}}>
        Tired of waiting?
      </div>
      <div style={{fontFamily: HEAD, fontWeight: 800, fontSize: 112, lineHeight: 1.02, letterSpacing: -3, color: C.light, marginBottom: 56}}>
        Book your scan.
      </div>
      <div
        style={{
          alignSelf: 'flex-start', transform: `scale(${btn * pulse})`, transformOrigin: 'left center',
          background: C.light, color: C.navy, fontFamily: HEAD, fontWeight: 800, fontSize: 50,
          borderRadius: 999, padding: '28px 56px', boxShadow: `0 20px 50px ${C.light}44`,
        }}
      >
        Link in bio · (727) 398-5999
      </div>
      <div style={{opacity: rest, marginTop: 56}}>
        <div style={{fontFamily: BODY, fontWeight: 600, fontSize: 38, color: C.white}}>Using insurance? We handle the authorization.</div>
        <div style={{fontFamily: BODY, fontSize: 25, lineHeight: 1.45, color: `${C.white}99`, marginTop: 30}}>
          Self-pay MRI price as of October 2026: without contrast, one body area ($395 with and without contrast). Insurance patients need a doctor&apos;s order. General information, not medical advice.
        </div>
      </div>
    </AbsoluteFill>
  );
};

export const Reel: React.FC = () => {
  useFonts();
  const seq = (k: keyof typeof S, el: React.ReactNode) => (
    <Sequence from={S[k][0]} durationInFrames={S[k][1] - S[k][0]}>
      {el}
    </Sequence>
  );
  return (
    <AbsoluteFill>
      <Background />
      {seq('hook', <Hook />)}
      {seq('wait', <Wait />)}
      {seq('turn', <Turn />)}
      {seq('perks', <Perks />)}
      {seq('price', <Price />)}
      {seq('end', <End />)}
    </AbsoluteFill>
  );
};
