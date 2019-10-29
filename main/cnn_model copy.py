from keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import backend as K
import os
import numpy as np



from tensorflow.python.keras.applications import InceptionV3, Xception
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense, GlobalAveragePooling2D

from tensorflow.python.keras.metrics import top_k_categorical_accuracy
from tensorflow.python.keras.optimizers import Adam
from sklearn.utils.class_weight import compute_class_weight

from collections import Counter
from keras.callbacks import CSVLogger, ModelCheckpoint



'''
학습 및 테스트 할 데이터 
'''
TRAIN_PATH = "dataset/train/"
batch_size = 128
input_shape = (200, 200)

datagen = ImageDatagenerator(rescale=1./255, validation_split=0.1)
generator_train = datagen.flow_from_directory(directory=TRAIN_PATH,
                                              target_size=input_shape,
                                              batch_size=batch_size,
                                              shuffle=True,
                                              subset="training")

generator_validate = datagen.flow_from_directory(directory=TRAIN_PATH,
                                                 target_size=input_shape,
                                                 batch_size=batch_size,
                                                 shuffle=False,
                                                 subset="validation")

#class weight 값 만들기.. 클래스 비율에 따른 가중치
counter = Counter(generator_train.classes)                          
max_val = float(max(counter.values()))
class_weight = {class_id : max_val/num_images for class_id, num_images in counter.items()}                     

# validation step size
steps_validate = generator_validate.n / batch_size

class Model():
    '''
    모델 클래스를 만들고 케라스에서 제공하는 어플리케이션 모듈을 사용.
    '''
    def __init__(self, name, class_weight, params):
        assert name != '', "Model name needs to be specified"
        self.name = name
        self.trained = False
        
    def construct_model(self):
        if self.name == 'inceptionv3':
            print('{:=^75}'.format('Downloading {}'.format(self.name)))
            print(params)
            self.base_model = InceptionV3(**params['network_params'])
            print('{:=^75}'.format('Download Complete'))
            
        elif self.name == 'xception':
            print('{:=^75}'.format('Downloading {}'.format(self.name)))
            self.base_model = Xception(**params['network_params'])
            print('{:=^75}'.format('Download Complete'))
            
            
        # 모델 구조  base model -> global average pooling -> dense
        print('{:=^75}'.format('Adding layers'))
        self.model = Sequential()
        self.model.add(self.base_model)
        self.model.add(GlobalAveragePooling2D())
        self.model.add(Dense(params['num_classes'], activation='softmax'))
        print('{:=^75}'.format('Added layers'))
        
        # 지정 경로에 저장
        if not os.path.exists('weight_path/'):
            os.mkdir('weight_path/')
        self.weight_save_path = os.path.join('weight_path/', self.name + "_weights.h5")
        
        print('{:=^75}'.format('Saving weights to {}'.format(self.weight_save_path)))
        self.model.save_weights(self.weight_save_path)
        print('{:=^75}'.format('Saved weights'))

    def train(self):
        if self.trained == True:
            self.model.load_weights(self.weight_save_path)
            self.trained = False
        assert params['mode'] in ['fe', 'ft'], "mode must be either 'fe' or 'ft'"

        # 레이어 trainable 지정
        # feature extraction
        if params['mode'] == 'fe':
            self.model.layers[0].trainable = False

        # finetuning
        elif params['mode'] == 'ft':
            self.model.layers[0].trainable = True
        #compile the model with designated parameters
        self.model.compile(optimizer=Adam(lr=params['lr']),
                            loss='categorical_crossentropy',
                            metrics=['categorical_accuracy'])

        if not os.path.exists(params['log_path']):
            os.mkdir(params['log_path'])

        if not os.path.exists(params['cp_path']):
            os.mkdir(params['cp_path'])

        # csv logger callback 
        log_path = os.path.join(params['log_path'], self.name + '_' + params['mode'] + '.log')
        csvlog_callback = CSVLogger(log_path)

        # checkpoint callback 
        cp_path = os.path.join(params['cp_path'], self.name + '_' + params['mode'] + '-{epoch:04d}-{val_loss:.2f}.h5')
        cp_callback = ModelCheckpoint(cp_path,
                                        mode="max",
                                        save_best_only=True)

        print('{:=^75}'.format('training {} with {}'.format(self.name, params['mode'])))
        # actual data fitting
        self.model.fit_generator(generator=generator_train,
                                    epochs=params['epoch'],
                                    class_weight=class_weight,
                                    validation_data=generator_validate,
                                    validation_steps=steps_validate,
                                    callbacks=[cp_callback, csvlog_callback])

        # save model once done training    
        if not os.path.exists(params['model_path']):
            os.mkdir(params['model_path'])

        model_save_path = os.path.join(params['model_path'], self.model.name + '_' + params['mode'] + '.h5')
        self.model.save(model_save_path)
        self.trained = True


# 아래 .flow() 함수는 임의 변환된 이미지를 배치 단위로 생성해서
# 지정된 'preview/' 폴더에 저장합니다.

def save_jpg(path,image_data):
    with open(path, 'wb') as f:
        f.write(image_data)

def make_jpg():
    '''
    이 함수를 실행시키면 기존 폴더에 있는 이미지들을 변형한 파일들을 생성시킨다.
    '''
    datagen = ImageDataGenerator(
            rotation_range=40,
            width_shift_range=0.2,
            height_shift_range=0.2,
            rescale=1./255,
            shear_range=0.2,
            zoom_range=0.2,#임의 축소 확대 범위
            horizontal_flip=False,#수평 뒤집기
            fill_mode='nearest',
            validation_split=0.1)
    path_dir = 'dataset/train/ㄷ/'
    save_dir = 'dataset/preview_ㄷ/'
    file_list = os.listdir(path_dir)


    for image in file_list:
        img = load_img(path_dir + image)  # PIL 이미지
        x = img_to_array(img)  # (3, 150, 150) 크기의 NumPy 배열
        x = x.reshape((1,) + x.shape)  # (1, 3, 150, 150) 크기의 NumPy 배열

        # 아래 .flow() 함수는 임의 변환된 이미지를 배치 단위로 생성해서
        # 지정된 'preview/' 폴더에 저장합니다.
        i = 0
        for batch in datagen.flow(x, batch_size=1, save_to_dir=save_dir, save_prefix='ㄱ', save_format='jpeg'):
            i += 1
            if i > 20:
                break  # 이미지 20장을 생성하고 마칩니다


# def train():
#     train_data_dir = 'data/train'

#     model = Sequential()
#     model.add(Conv2D(32, (3, 3), input_shape=(3, 150, 150)))
#     model.add(Activation('relu'))
#     model.add(MaxPooling2D(pool_size=(2, 2)))

#     model.add(Conv2D(32, (3, 3)))
#     model.add(Activation('relu'))
#     model.add(MaxPooling2D(pool_size=(2, 2)))

#     model.add(Conv2D(64, (3, 3)))
#     model.add(Activation('relu'))
#     model.add(MaxPooling2D(pool_size=(2, 2)))


#     model.add(Flatten())  # 이전 CNN 레이어에서 나온 3차원 배열은 1차원으로 뽑아줍니다
#     model.add(Dense(64))
#     model.add(Activation('relu'))
#     model.add(Dropout(0.5))
#     model.add(Dense(2))
#     model.add(Activation('sigmoid'))

#     model.compile(loss='categorical_crossentropy',
#                 optimizer='rmsprop',
#                 metrics=['accuracy'])
#     print("데이터 셋의 이미지를 트레이닝 하는 함수 ")


categories = ["ㄱ", "ㄴ", "ㄷ"]
num_classes = len(categories)
params = {
    'num_classes': num_classes, # 카테고리 수
    'log_path': 'log/', # 로그 파일 저장 경로
    'cp_path': 'checkpoint/', # 모델 체크포인트 저장 경로
    'model_path': 'model/', # 최종 모델 저장 경로
    'mode': 'fe', # 훈련 모드 (fe: feature extraction, ft: finetuning)
    'lr': 0.001, # learning rate
    'epoch': 10, # 훈련 epoch
    'network_params': { # applications 모듈로 불러들일 네트워크 파라미터
        'include_top' : False, 
        'weights' : 'imagenet', 
        'input_shape' : input_shape + (3,)
    }
}
def train_model_class():


    inception = Model(name='inceptionv3', class_weight=class_weight, params=params)
    #xception = Model(name='xception', class_weight=class_weight, params=params)

    inception.construct_model()
    #xception.construct_model()
    inception.construct_model
    inception.train
    inception.train()
    #xception.train()

def predict():
    print("이미지가 넘어 오면 모델을 예측해서 반환 해주는 함수")

train_model_class()