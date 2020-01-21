from keras.models import Model
from keras.layers import Input, Lambda
import numpy as np
from keras import backend as K
from keras.models import load_model
from keras.layers import Input
from yolo3.model import preprocess_true_boxes, yolo_body, tiny_yolo_body, yolo_loss
filename='test1.h5'

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

model_body = yolo_body(image_input, 3, 20)
print (model_body)

h, w = [248, 248]
num_anchors=9
num_classes=20
y_true = [Input(shape=(h//{0:32, 1:16, 2:8}[l], w//{0:32, 1:16, 2:8}[l], \
        num_anchors//3, num_classes+5)) for l in range(3)]


model_loss = Lambda(yolo_loss, output_shape=(1,), name='yolo_loss',
        arguments={'anchors': anchors, 'num_classes': num_classes, 'ignore_thresh': 0.5})(
        [*model_body.output, *y_true])

model = Model([model_body.input, *y_true], model_loss)

model.save(filename)
#model_body.save(filename)
