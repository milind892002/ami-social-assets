import React, {useEffect, useState} from 'react';
import {continueRender, delayRender, staticFile} from 'remotion';

export const C = {
  navy: '#0B2440',
  deep: '#12355C',
  blue: '#1D5FA6',
  light: '#9CC6F0',
  white: '#FFFFFF',
  amber: '#F5B841',
  green: '#5FD3A8',
};

const FACES: [string, string, number][] = [
  ['Inter', 'inter-latin-400-normal.woff2', 400],
  ['Inter', 'inter-latin-600-normal.woff2', 600],
  ['Inter', 'inter-latin-700-normal.woff2', 700],
  ['Inter', 'inter-latin-800-normal.woff2', 800],
  ['DM Sans', 'dm-sans-latin-600-normal.woff2', 600],
  ['DM Sans', 'dm-sans-latin-700-normal.woff2', 700],
  ['DM Sans', 'dm-sans-latin-800-normal.woff2', 800],
];

export const useFonts = () => {
  const [handle] = useState(() => delayRender('fonts'));
  useEffect(() => {
    Promise.all(
      FACES.map(([family, file, weight]) => {
        const f = new FontFace(family, `url(${staticFile(file)})`, {weight: String(weight)});
        return f.load().then((loaded) => document.fonts.add(loaded));
      }),
    ).then(() => continueRender(handle));
  }, [handle]);
};

export const HEAD = "'DM Sans', sans-serif";
export const BODY = "'Inter', sans-serif";

export const Check: React.FC<{size?: number; color?: string}> = ({size = 72, color = C.green}) => (
  <svg width={size} height={size} viewBox="0 0 24 24">
    <circle cx="12" cy="12" r="11" fill={color} />
    <path d="M7 12.5l3.2 3.2L17 9" stroke={C.navy} strokeWidth="2.6" fill="none" strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);
