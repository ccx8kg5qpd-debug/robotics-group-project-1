# Formal Jetson Test Results

The formal test uses the first 20 saved frames from the final Jetson session on 31 August 2026, ordered by capture time. A frame is counted as correct only when every visible target is detected with the correct class. No incorrect class assignment occurred in this session; all failed frames are partial missed detections.

## Summary

- Formal test frames: 20
- Correct frames: 17
- Failed frames: 3
- Frame-level accuracy: `17 / 20 x 100% = 85.00%`
- Required accuracy: at least 80%
- Result: requirement met

## Full-loop FPS

- Minimum: 16.7 FPS
- Maximum: 25.8 FPS
- Arithmetic mean: 22.20 FPS
- Required speed: at least 5 FPS
- Result: requirement met

FPS values are read directly from the saved Jetson frames. The program calculates a 30-frame moving average from complete loop intervals, covering camera capture, inference, annotation, display, and event handling rather than converting model-only inference time.

## Error analysis

The three failed formal frames contain correctly classified detections but miss one visible mouse:

1. `error_reclassified_20260831_215645_674393.jpg`: two of three mice detected.
2. `error_20260831_215703_550940.jpg`: two bottles and two of three mice detected.
3. `error_20260831_215714_021213.jpg`: two bottles and one of two mice detected.

An additional saved frame, `error_20260831_215718_819397.jpg`, is retained as a supplementary error example and is not included in the 20-frame accuracy calculation. It also contains a missed mouse and no wrong-class prediction.

The per-frame classes, confidence values, FPS values, and decisions are recorded in `test_20_results.csv`.
