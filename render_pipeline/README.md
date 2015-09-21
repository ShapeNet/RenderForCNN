Render for CNN: the rendering pipeline

Three stages:
 - Render synthetic images of objects through overfit-resistant rendering, see `render_model_views.py`
 - Crop images according to statistics learnt from KDE on real images, see `crop_gray.m`
 - Overlay background to the cropped images, see `overlay_background.m`

demo/: small scale demo of the render4cnn pipeline
kde/: use kernel density estimation to get statistics of viewpoint and truncation patterns
