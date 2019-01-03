import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.optimizers import SGD

from sklearn.utils import shuffle   # softmax 함수에서 사용



def logitic_sigmoid():
    # 모델 생성
    m_model = Sequential([])
    m_model.add(Dense(input_dim=2, units=1))
    m_model.add(Activation('sigmoid'))

    m_model.compile(loss='binary_crossentropy', optimizer=SGD(lr=0.1))

    #모델 학습
    m_x = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    m_y = np.array([[0], [1], [1], [1]])

    m_model.fit(m_x, m_y, epochs=200, batch_size=1)

    m_classes = m_model.predict_classes(m_x, batch_size=1)
    m_prob = m_model.predict_proba(m_x, batch_size=1)


    print('classified:')
    print(m_y == m_classes)
    print()
    print('ouput probability:')
    print(m_prob)

def softmax():

    m_input_dimen_cnt = 2                   # 입력 데이터의 차원
    m_class_cnt = 3                         # 클래스 수
    m_class_in_cnt = 100                    # 클래스에 있는 데이터 수
    m_total = m_class_in_cnt * m_class_cnt  # 전체 데이터 수


    # 학습 데이터
    m_x1 = np.random.randn(m_class_in_cnt, m_input_dimen_cnt) + np.array([0, 10])
    m_x2 = np.random.randn(m_class_in_cnt, m_input_dimen_cnt) + np.array([5, 5])
    m_x3 = np.random.randn(m_class_in_cnt, m_input_dimen_cnt) + np.array([5, 5])

    m_y1 = np.array([[1, 0, 0] for i in range(m_class_in_cnt)])
    m_y2 = np.array([[0, 1, 0] for i in range(m_class_in_cnt)])
    m_y3 = np.array([[0, 0, 1] for i in range(m_class_in_cnt)])

    m_x = np.concatenate((m_x1, m_x2, m_x3), axis=0)
    m_y = np.concatenate((m_y1, m_y2, m_y3), axis=0)


    # 모델 생성
    m_model = Sequential([])
    m_model.add(Dense(input_dim=m_input_dimen_cnt, units=m_class_cnt))
    m_model.add(Activation('softmax'))

    m_model.compile(loss='categorical_crossentropy', optimizer=SGD(lr=0.1))

    m_model.fit(m_x, m_y, epochs=20, batch_size=50)

    m_xc, m_yc = shuffle(m_x, m_y)
    m_classes = m_model.predict_classes(m_xc[0:10], batch_size=50)
    m_prob = m_model.predict_proba(m_xc[0:10], batch_size=50)

    print('classified:')
    print(np.argmax(m_model.predict(m_xc[0:10]), axis=1) == m_classes)
    print()
    print('output probability:')
    print(m_prob)


logitic_sigmoid()