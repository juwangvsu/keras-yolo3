model_data/yolo.h5  		--- converted from pretrained with coco data set, can be loaded by 
					code1/keras-yolo3/predict.py
				python3 convert.py yolov3.cfg yolov3.weights model_data/yolo.h5
model_data/yolov3-voc_9000.h5	--- converted from yolov3-voc_9000.weights, trained with voc under darknet
					detection box good

logs/000/trained_weights_final.h5-- local train with voc dataset, fail load by code1/keras-yolo3/predict.py, probably missing structure info, save_weights_only=True at train.py, testing

------------------code reading------------------
yolo.py
	define YOLO class, which is a wrapper of yolo3 modela
	pass .h5 file
	perform load_model, or load_weights and return a model
	if load_model fail, it will load_weight
		if has to load_weights, first use yolo3/model's yolo_body 
		to create an instance of Model, then load weights.

yolo3/model.py
	define the yolo_body, which is the yolo3 model, all layers

yolo_video.py
	yolo.YOLO(..)

train.py
	call yolo_body to create Model, then load_weights,
	it did not use load_model

-------------------1/20/2020 checkpoint .h5 bug  ---------------
Issue:
	Prio to this fix, the saved .h5  fail load_model(), in both code1/keras-yolo3/predict.py and test_load_model.py here.

with ModelCheckpoint, save_weights_only = False, result in a huge file
with ModelCheckpoint, save_weights_only = True, result in 250mb, but not loadable by code1/keras-yolo3$ python3 predict.py
with CustomizedCheckpoint, result in 490 mb

ep1016-loss20.451-val_loss32.877.h5 
	use CustomizedCheckpoint, load fail NameError: name 'yolo_head' is not defined
	this file contain model arch data, but still error, 
other .h5 in logs/000 does not contain arch data, error about readonly..Cannot create group in read-only mode.

fixed:
	model.save() vs model_to_save.save()
	the reason is because the saved model by the train.py use model.save().
	model is the training model, model_to_save is the infer model.
	in the other package code1/keras-yolo3/train.py, the equivalent models are train_model and
	infer_model, and infer_model is the one that is saved.

	in this package's train.py, the load_model() actually fail and load_weights() is then called. that is the bug
	the original author did not fix.


----------------------training performance ---------------------

train t3 stall, loss value stuck at 8.xx
Epoch 1200/1200
562/562 [==============================] - 128s 227ms/step - loss: 8.5948 - val_loss: 9.5883

homepc, titan, batch size 16,
Epoch 1167/2000
70/70 [==============================] - 103s 1s/step - loss: 7.8393 - val_loss: 29.9031

Epoch 1400, still no improvemnt

-----------------1/7/2020 detection with yolo_video.py--------
python3 yolo_video.py --model_path model_data/yolo.h5 --classes_path model_data/coco_classes.txt --image
python3 yolo_video.py --model_path model_data/yolov3-voc_9000.h5 --classes_path model_data/voc_classes.txt --image
python3 yolo_video.py --model_path logs/000/trained_weights_final.h5 --classes_path model_data/voc_classes.txt --image
	interactive provide filename e.g dog2.jpg

bug fixed:
	msi, modify yolo.py with 
	config.gpu_options.allow_growth = True

	yolo_video.py: --model replaced by --model_path, --classes replaced by --classes_path

	.h5 file and the voc_classes.txt must match. default coco_classes.txt match model_data/yolo.h5, which
	is trained with 80 classes coco data. the retrained logs/000/trained_weights_final.h5 use voc2007 data

-----------------1/7/2020 training from a previous step--------
msi, sda19, tf14-gpu
(t1) python3 train.py --weights_file logs/000/trained_weights_stage_1.h5 --phase_i 2
(t2) python3 train.py --weights_file logs/000/trained_weights_final.h5 --phase_i 2
(t3) python3 train.py --weights_file logs/000/trained_weights_final.h5 --phase_i 1 --skip_phasei True
(t4) python3 train.py --weights_file model_data/yolov3-voc_9000.h5 --phase_i 1 --skip_phasei True

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

train t3 stall, loss value stuck at 8.xx
Epoch 1200/1200
562/562 [==============================] - 128s 227ms/step - loss: 8.5948 - val_loss: 9.5883

bug:
	gpu memory problem with rtx 2080, this seems to be common on rtx 20xx,
	error msg is: 
        the code works on msi, but not on rtx 2080. error msg "CUDNN_STATUS_INTERNAL_ERROR",
	tred to fix by "config.gpu_options.allow_growth = True" 
		cause an error "The Session graph is empty.". notice this
		is not the problem with /media/student/code1/faster_rcnn which also use keras

fixed: (partial)
	for rtx 2080, this bug is fixed by comment off this line:
		   K.clear_session() # get a new session
		in train.py::create_model(), this seems work, and the training proceed.
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
