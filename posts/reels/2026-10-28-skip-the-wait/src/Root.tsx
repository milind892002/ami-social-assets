import React from 'react';
import {Composition, Still} from 'remotion';
import {Reel, REEL_FRAMES} from './Reel';
import {Gbp} from './Gbp';

export const RemotionRoot: React.FC = () => (
  <>
    <Composition id="Reel" component={Reel} durationInFrames={REEL_FRAMES} fps={30} width={1080} height={1920} />
    <Still id="Gbp" component={Gbp} width={1200} height={900} />
  </>
);
