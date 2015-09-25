Render for CNN: demo of usages of the off-the-shelf viewpoint estiamtor on images of objects in PASCAL3D+ classes.

    python run_demo.py

To visualize the viewpoint by rendering an object in the estimated viewpoint:

    python run_visualize_3dview.py

reference results (estimated view and rendered image of an object in that view) are in `ref_output`.

*NOTE:* You can change input image filename in `run_demo.py` and CAD model path in `run_visualize_3dview.py` to run demo on different image of other object in PASCAL3D_ classes. For batch processing, you would create a list of image filenames and a list of their class indices (can be acquired by `g_shape_names.index(<name>)`) and use the `viewpoint` function as in `run_demo.py`.
