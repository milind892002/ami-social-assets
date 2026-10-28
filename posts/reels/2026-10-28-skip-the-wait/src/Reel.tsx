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
  dont: [0, 60],
  hook: [60, 170],
  wait: [170, 290],
  care: [290, 395],
  notwhat: [395, 500],
  perks: [500, 610],
  price: [610, 705],
  end: [705, 825],
} as const;
export const REEL_FRAMES = 825;

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

// ---------- Big blunt type ----------
type Line = {t: string; size: number; color?: string; delay: number};
const BigLines: React.FC<{len: number; lines: Line[]; eyebrow?: string}> = ({len, lines, eyebrow}) => {
  const {opacity, f} = useInOut(len, 8);
  const {fps} = useVideoConfig();
  return (
    <AbsoluteFill style={{opacity, justifyContent: 'center', paddingLeft: PAD_L, paddingRight: PAD_R}}>
      {eyebrow ? (
        <div style={{fontFamily: BODY, fontWeight: 800, fontSize: 36, letterSpacing: 6, color: C.light, marginBottom: 30, opacity: interpolate(f, [0, 10], [0, 1], clamp)}}>{eyebrow}</div>
      ) : null}
      {lines.map((l) => {
        const sp = spring({frame: f - l.delay, fps, config: {damping: 13, stiffness: 190}});
        return (
          <div key={l.t} style={{overflow: 'hidden', paddingBottom: 6}}>
            <div style={{transform: `translateY(${(1 - sp) * 110}%)`, fontFamily: HEAD, fontWeight: 800, fontSize: l.size, lineHeight: 1.0, letterSpacing: -l.size * 0.025, color: l.color ?? C.white}}>
              {l.t}
            </div>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

const Dont: React.FC = () => {
  const len = S.dont[1] - S.dont[0];
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const a = spring({frame: f, fps, config: {damping: 10, stiffness: 260}});
  const b = spring({frame: f - 8, fps, config: {damping: 10, stiffness: 260}});
  const out = interpolate(f, [len - 6, len], [1, 0], clamp);
  return (
    <AbsoluteFill style={{opacity: out, justifyContent: 'center', paddingLeft: PAD_L, paddingRight: PAD_R}}>
      <div style={{fontFamily: HEAD, fontWeight: 800, fontSize: 250, lineHeight: 0.92, letterSpacing: -8, color: C.white, transform: `scale(${1.4 - 0.4 * a})`, transformOrigin: 'left center', opacity: a}}>DON&apos;T</div>
      <div style={{fontFamily: HEAD, fontWeight: 800, fontSize: 250, lineHeight: 0.92, letterSpacing: -8, color: C.light, transform: `scale(${1.4 - 0.4 * b})`, transformOrigin: 'left center', opacity: b}}>WAIT.</div>
    </AbsoluteFill>
  );
};

const HookLines: React.FC = () => (
  <BigLines
    len={S.hook[1] - S.hook[0]}
    lines={[
      {t: 'for your', size: 112, delay: 2},
      {t: 'insurance to', size: 112, delay: 7},
      {t: 'tell you when', size: 112, delay: 12},
      {t: 'you can get', size: 112, delay: 17},
      {t: 'your MRI or', size: 112, color: C.light, delay: 22},
      {t: 'imaging scan.', size: 112, color: C.light, delay: 27},
    ]}
  />
);

const Care: React.FC = () => (
  <BigLines
    len={S.care[1] - S.care[0]}
    lines={[
      {t: 'WE OFFER', size: 150, delay: 0},
      {t: 'YOU THE', size: 150, delay: 6},
      {t: 'CARE YOU', size: 150, color: C.light, delay: 12},
      {t: 'DESERVE.', size: 150, color: C.light, delay: 18},
    ]}
  />
);

const NotWhat: React.FC = () => (
  <BigLines
    len={S.notwhat[1] - S.notwhat[0]}
    lines={[
      {t: 'Not what your', size: 112, delay: 0},
      {t: 'insurance', size: 112, color: C.amber, delay: 6},
      {t: 'company', size: 112, color: C.amber, delay: 12},
      {t: 'wants you', size: 112, delay: 18},
      {t: 'to have.', size: 112, delay: 24},
    ]}
  />
);

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
      <div style={{fontFamily: HEAD, fontWeight: 800, fontSize: 64, lineHeight: 1.04, color: C.white}}>{text}</div>
    </div>
  );
};

const Perks: React.FC = () => {
  const len = S.perks[1] - S.perks[0];
  const {opacity} = useInOut(len);
  return (
    <AbsoluteFill style={{opacity, justifyContent: 'center', paddingLeft: PAD_L, paddingRight: PAD_R}}>
      <div style={{fontFamily: BODY, fontWeight: 700, fontSize: 34, letterSpacing: 5, color: C.light, marginBottom: 20}}>AT ADVANCED MEDICAL IMAGING</div>
      <div style={{fontFamily: HEAD, fontWeight: 800, fontSize: 110, lineHeight: 1.0, color: C.white, marginBottom: 54}}>
        Self-pay.<br /><span style={{color: C.light}}>No waiting.</span>
      </div>
      <Perk text="No referral needed" delay={10} />
      <Perk text="No prior authorization" delay={24} />
      <Perk text="Same-day scans, often" delay={38} />
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
      <div style={{fontFamily: HEAD, fontWeight: 800, fontSize: 140, lineHeight: 1.0, letterSpacing: -4, color: C.white}}>
        YOUR SCAN.
      </div>
      <div style={{fontFamily: HEAD, fontWeight: 800, fontSize: 140, lineHeight: 1.0, letterSpacing: -4, color: C.light, marginBottom: 56}}>
        YOUR SCHEDULE.
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
        <div style={{fontFamily: BODY, fontWeight: 600, fontSize: 40, color: C.white}}>Insurance accepted too.</div>
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
      {seq('dont', <Dont />)}
      {seq('hook', <HookLines />)}
      {seq('wait', <Wait />)}
      {seq('care', <Care />)}
      {seq('notwhat', <NotWhat />)}
      {seq('perks', <Perks />)}
      {seq('price', <Price />)}
      {seq('end', <End />)}
    </AbsoluteFill>
  );
};
