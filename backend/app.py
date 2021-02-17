import numpy as np
np.random.seed(42)
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Activation
from tensorflow.keras.layers import LSTM, Dropout
from tensorflow.keras.layers import TimeDistributed
from tensorflow.keras.optimizers import RMSprop
import pickle
import sys
import heapq
import time
from flask import Flask, render_template
from flask_socketio import SocketIO, emit,send

#import data
SEQUENCE_LENGTH=40
step=3
model = load_model('module/keras_model.h5')
history = pickle.load(open("module/history.p", "rb"))
path="module/nietzsche.txt"
#bin of words
text=open(path).read().lower()
print(len(text))
chars=sorted(list(set(text)))
char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char=dict((i, c) for i, c in enumerate(chars))
print(f'unique chars: {len(chars)}')


def sample(preds,top_n=3):
    preds=np.asarray(preds).astype('float64')
    preds=np.log(preds)
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    return heapq.nlargest(top_n, range(len(preds)), preds.take)

def prepare_input(text):
    x=np.zeros((1,SEQUENCE_LENGTH,len(chars)))
    for t,char in enumerate(text):
        x[0,t,char_indices[char]]=1
    return x


def predict_completion(text):
    original_text = text
    generated = text
    completion = ''
    while True:
        x = prepare_input(text)
        preds = model.predict(x, verbose=0)[0]
        next_index = sample(preds, top_n=1)[0]
        next_char = indices_char[next_index]
        text = text[1:] + next_char
        completion += next_char
        if len(original_text + completion) + 2 > len(original_text) and next_char == ' ':
            return completion
def predict_completions(text, n=3):
    if len(text)>=SEQUENCE_LENGTH:    
        x = prepare_input(text)
        preds = model.predict(x, verbose=0)[0]
        next_indices = sample(preds, n)
        return [indices_char[idx] + predict_completion(text[1:] + indices_char[idx]) for idx in next_indices]
    else:
        return("length of text should be greater then 40")


the_text="That which does not kill us makes us stronger."
seq = the_text[:40].lower()
predict_list=None



app = Flask(__name__)
GLOBAL_FILTER=[]




socketio = SocketIO(app,cors_allowed_origins="*")
@socketio.on('filter change')
def value_change(message):
    last_40=message["filter"][-40:].lower()
    print(last_40)
    datatosend={"prediction":predict_completions(last_40)}
    emit('event',datatosend,broadcast=True)
    socketio.sleep(0)




@socketio.on('connect')
def client_connect():
    print(predict_list)

@socketio.on('disconnect')
def client_disconnect():
    print("disconnected")

if __name__ == '__main__':
    socketio.run(app,port=5000,debug=True)