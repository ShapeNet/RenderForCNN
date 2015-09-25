Render for CNN: viewpoint estimator

To prepare testing images, run:

    python prepare_testing_images.py

To do evaluation (AVP-NV of VOC12 val images and Acc-pi/6 and MedErr on VOC12 val non-truncated and non-occluded images), run:

    python run_evaluation

For usages of the off-the-shelf viewpoint estimator, see `../demo_view` for an example.
ref output of evaluation is in `ref_evaluation_results`.
