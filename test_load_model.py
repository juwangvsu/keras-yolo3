from keras.layers import Input, Lambda
import numpy as np
from keras import backend as K
from keras.models import load_model
from keras.layers import Input
from yolo3.model import preprocess_true_boxes, yolo_body, tiny_yolo_body, yolo_loss
#filename='test1.h5'
#filename='logs/000/ep1016-loss24.099-val_loss39.484.h5'
filename='epp1016-val_loss27.288.h5'

anchors = [ 10. , 13.
, 16.,  30.
, 33.,  23.
, 30.,  61.
, 62.,  45.
, 59., 119.
,116.,  90.
,156., 198.
, 373., 326.]

anchors = np.array(anchors).reshape(-1, 2)
image_input = Input(shape=(None, None, 3))

model=load_model(filename)

print(model)
