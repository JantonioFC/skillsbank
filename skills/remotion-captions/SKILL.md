---
name: remotion-captions
description: Transcribing, displaying and animating captions
version: 4.0.543
metadata:
  tags: subtitles, captions, remotion, json
risk: safe
source: https://github.com/remotion-dev/skills
source_repo: remotion-dev/skills
source_type: official
date_added: '2026-11-15'
license: unspecified
---

All captions must be processed in JSON. The captions must use the [`Caption`](https://www.remotion.dev/docs/captions/caption.md) type which is the following:

```ts
import type { Caption } from "@remotion/captions";
```

This is the definition:

```ts
type Caption = {
  text: string;
  startMs: number;
  endMs: number;
  timestampMs: number | null;
  confidence: number | null;
  pageBreakAfter?: boolean;
};
```

## Generating captions

To transcribe video and audio files to generate captions, load the [transcribe-captions.md](transcribe-captions.md) file for more instructions.

## Displaying captions

To display captions in your video, load the [display-captions.md](display-captions.md) file for more instructions.

## Importing captions

To import captions from a .srt file, load the [import-srt-captions.md](import-srt-captions.md) file for more instructions.

## Post-creation

After you're done, load this skill: Remotion Best Practices (`remotion-best-practices` skill)

If not already done, open the Remotion Studio, unless instructed otherwise.

## When to Use

- Transcribing, displaying and animating captions
- Working with **Generating captions**
- Working with **Displaying captions**
- Working with **Importing captions**
- Working with **Post-creation**
