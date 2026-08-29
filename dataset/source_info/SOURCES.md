# Dataset sources

## COCO 2017

- Dataset: Microsoft COCO 2017 object-detection train/validation splits
- Project URL: https://cocodataset.org/
- AWS Open Data mirror used for annotation archive: https://registry.opendata.aws/fast-ai-coco/
- Image download pattern: `http://images.cocodataset.org/{split}2017/{file_name}`
- Annotation file: `instances_train2017.json` and `instances_val2017.json` from `annotations_trainval2017.zip`
- Downloaded into the formal dataset: **970 images** (379 bottle-only, 379 mouse-only, 212 containing both)
- Category mapping: COCO `bottle` (category 44) -> YOLO class 0; COCO `mouse` (category 74, computer mouse) -> YOLO class 1
- Bounding boxes: COCO instance bounding boxes converted to normalized YOLO detection format

COCO images retain their individual Flickr Creative Commons licenses. The exact source URL, Flickr URL, license name, license URL, COCO image ID, split, SHA-256, and quality metrics for every retained image are recorded in `source_manifest.csv`.

License distribution among retained images:

- CC BY-NC-SA 2.0: 420
- CC BY 2.0: 219
- CC BY-NC 2.0: 179
- CC BY-SA 2.0: 152

All CC BY-ND and CC BY-NC-ND images were excluded because model-training/format-conversion treatment under a NoDerivs license is uncertain. The retained NC-licensed subset is suitable only for non-commercial research use unless separate permission is obtained. Attribution and ShareAlike obligations still apply; consult `source_manifest.csv` before redistribution.

## Existing user dataset

The 30 images in `~/desk-object-labeling/labeled` were read only for cross-dataset duplicate comparison. They were not copied, changed, or counted among the 970 external images. Combined intended project scale: 30 existing + 970 external = **1000 images**.
