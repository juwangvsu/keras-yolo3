
If you want to use original pretrained weights for YOLOv3:
0. python3 voc_annotation.py , this create annotate data file from VOCdevkit 
1. wget https://pjreddie.com/media/files/darknet53.conv.74
2. rename it as darknet53.weights
3. python3 convert.py -w darknet53.cfg darknet53.weights model_data/darknet53_weights.h5
4. use model_data/darknet53_weights.h5 in train.py

trainging results:
	log/000/
module 'keras.backend' has no attribute 'control_flow_ops'
fix:
	tf.while_loop working here, using tensorflow 1.14.0
