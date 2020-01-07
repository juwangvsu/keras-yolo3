
-----------------1/7/2020 training from a previous step--------
msi, sda19, tf14-gpu
(t1) python3 train.py --weights_file logs/000/trained_weights_stage_1.h5 --phase_i 2
(t2) python3 train.py --weights_file logs/000/trained_weights_final.h5 --phase_i 2

	-phase_i : number of epoch for phase i, default 50
	-weights_file: initial weights

run out of memory at phase 2, set 
	batch_size=4 ok

train t2 run glance:
	msi, 1060
	Epoch 1/2 115s 2s/step - loss: 20.9541 - val_loss: 17.2898
	Epoch 52/100
	562/562 [==============================] - 314s 559ms/step - loss: 28.4765 - val_loss: 25.5125

	rtx2080:
	Epoch 1/2 109s 2s/step - loss: 20.8288 - val_loss: 26.3043
	Epoch 2/2 118s 2s/step - loss: 21.1164 - val_loss: 19.2494
	Epoch 51/100
	562/562 [==============================] - 145s 259ms/step - loss: 26.8667 - val_loss: 22.0058

bug:
	gpu memory problem with rtx 2080, this seems to be common on rtx 20xx,
	the fix config.gpu_options.allow_growth = True 
		cause an error "The Session graph is empty.". notice this
		is not the problem with /media/student/code1/faster_rcnn which also use keras

fixed: (partial)
	for rtx 2080, this bug is fixed by comment off this line:
		   K.clear_session() # get a new session
		in train.py::create_model()
		not sure how it will affect the rest of the code.
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
