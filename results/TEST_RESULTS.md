# Two-Session Jetson Test Results

Two complete Jetson test sessions are retained. A frame is counted as correct only
when every visible target is detected with the correct class. Failed frames are
included in every calculation; no result was removed to improve the reported rate.

## Session 1 — baseline scenes, 29 August 2026

The first session contains mostly single-object scenes and simpler bottle-and-mouse
combinations.

- Formal frames: 22
- Correct frames: 21
- Failed frames: 1
- Accuracy: `21 / 22 x 100% = 95.45%`
- Full-loop FPS: 16.6-16.9, arithmetic mean 16.77

The single failure is `error_20260829_201227_163337.jpg`. The mouse is detected
correctly, but the horizontal bottle is missed. It is a false-negative case rather
than a wrong-class prediction.

## Session 2 — more complex scenes, 31 August 2026

The second session deliberately increases scene difficulty. It contains more
objects in the same frame, including up to three mice and scenes with two bottles
and multiple mice. The layouts, object distances, and viewpoints are more varied
than in Session 1. This makes partial occlusion and missed detection more likely.

- Formal frames: 20
- Correct frames: 17
- Failed frames: 3
- Accuracy: `17 / 20 x 100% = 85.00%`
- Full-loop FPS: 16.7-25.8, arithmetic mean 22.20

The three formal failures are partial missed detections of one mouse:

1. `error_reclassified_20260831_215645_674393.jpg`: two of three mice detected.
2. `error_20260831_215703_550940.jpg`: two bottles and two of three mice detected.
3. `error_20260831_215714_021213.jpg`: two bottles and one of two mice detected.

`error_20260831_215718_819397.jpg` is retained as a supplementary error example but
is excluded from the formal calculations. It was saved after the first 20
chronological frames and shows the same missed-mouse failure mode.

## Combined result

| Scope | Frames | Correct | Failed | Accuracy | Mean FPS |
|---|---:|---:|---:|---:|---:|
| Session 1 | 22 | 21 | 1 | 95.45% | 16.77 |
| Session 2, more complex | 20 | 17 | 3 | 85.00% | 22.20 |
| Combined | 42 | 38 | 4 | 90.48% | 19.35 |

The combined accuracy exceeds the required 80%, and every formal frame exceeds the
required 5 FPS. The lower accuracy in Session 2 is interpreted in the context of
its deliberately more difficult multi-object scenes; it does not result from a
model or confidence-threshold change between the two tests.

## Record files

- `test_session_1_22_results.csv`: complete Session 1 record
- `test_session_2_20_results.csv`: complete Session 2 record
- `test_20_results.csv`: retained compatibility copy of the Session 2 record
- `combined_42_results.csv`: all 42 formal frames
- `test_summary.csv`: per-session and combined metrics

The evidence directories contain 38 formal correct-case images and five retained
error images. Four error images belong to the 42-frame calculation; the fifth is
the explicitly identified supplementary Session 2 frame.
