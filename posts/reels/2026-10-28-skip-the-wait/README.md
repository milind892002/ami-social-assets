Remotion source for the 2026-10-28 "Skip the wait" Reel (1080x1920, 21 s, 30 fps, silent).

    npm i remotion@4.0.539 @remotion/cli@4.0.539 react@18.3.1 react-dom@18.3.1
    cp ~/.cache/ami-fonts/node_modules/@fontsource/{inter,dm-sans}/files/*-latin-{400,600,700,800}-normal.woff2 public/
    npx remotion render src/index.ts Reel out/reel.mp4 --codec=h264 --crf=18 --browser-executable=$(node -e "console.log(require('playwright').chromium.executablePath())")
    npx remotion still src/index.ts Gbp out/gbp.png   # Google image 1200x900
