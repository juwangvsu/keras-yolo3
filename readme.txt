
-----------------1/7/2020 training from a previous step--------
msi, sda19, tf14-gpu
python3 train.py --weights_file logs/000/trained_weights_stage_1.h5 --phase_i 2
python3 train.py --weights_file logs/000/trained_weights_final.h5 --phase_i 2

	-phase_i : number of epoch for phase i, default 50
	-weights_file: initial weights

run out of memory at phase 2, set 
	batch_size=4 ok

train rst glance:
	562/562 [==============================] - 318s 566ms/step - loss: 31.3958 - val_loss: 18.2914
	Epoch 52/100
	562/562 [==============================] - 314s 559ms/step - loss: 28.4765 - val_loss: 25.5125

-----------------1/6/2020 training steps------------------------
If you want to use original pretrained weights for YOLOv3:
0. python3 voc_annotation.py , this create annotate data file from VOCdevkit 
1. wget https://pjreddie.com/media/files/darknet53.conv.74
2. rename it as darknet53.weights
3. python3 convert.py -w darknet53.cfg darknet53.weights model_data/darknet53_weights.h5
4. use model_data/darknet53_weights.h5 in train.py
5. logs/000$ tensorboard --logdir .

trainging results:
	log/000/
module 'keras.backend' has no attribute 'control_flow_ops'
fix:
	tf.while_loop working here, using tensorflow 1.14.0
