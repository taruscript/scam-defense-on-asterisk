from flask import Flask, request, Blueprint, jsonify
import speech_recognition as sr
import os
import MeCab
from gensim.models import word2vec
from gensim.models import KeyedVectors

# Blueprintオブジェクトを生成
app = Blueprint('input_data', __name__)

model = KeyedVectors.load_word2vec_format('apps/word_model/entity_vector.model.bin', binary=True)
# model = KeyedVectors.load_word2vec_format('apps/word_model/entity_vector.model.bin')
tagger = MeCab.Tagger("-d /usr/local/lib/mecab/dic/ipadic")
tagger.parse("")



# index にアクセスされた場合の処理
@app.route('/scam_check', methods=['POST'])
def input_data():
    if 'file' not in request.files:
        return "ファイル未指定"
    
    fs = request.files['file']
    
    # ファイルを保存
    save_path = f"upload/{fs.filename}"
    fs.save(save_path)

    audio_recognized = voice_recognize(save_path)
    scam_result =  scam_check(audio_recognized)
    # return jsonify(scam_result)
    return jsonify({"msg":"sucess"})

def voice_recognize(save_path):
    print("音声認識を開始します") 
    r = sr.Recognizer()
    with sr.AudioFile(save_path) as source:
        audio = r.record(source)
    try:
        result_recognized = r.recognize_google(audio, language='ja-JP')
    except speech_recognition.UnknownValueError:
        print("音声認識ができませんでした")
        return None
    return result_recognized

# 特殊詐欺を検知する
def scam_check(text):
    print(text)
    #渡されたテキストを形態素解析
    node = tagger.parseToNode(text)
    scores = []
    word = []
    # 特殊詐欺に使われそうな語群
    keywords = ['銀行','警察']
    while node is not None:
        fields = node.feature.split(",")
        if fields[0] == '名詞' or fields[0] == '動詞' or fields[0] == '形容詞':   
            try:
                for keyword in keywords:
                    scores.append(model.wv.similarity(node.surface, keyword))
                word.append(node.surface)
            except KeyError:
                pass
            
        node = node.next
    highcore_index = scores.index(max(scores)) // len(keywords)
    highscore_word = word[highcore_index]

    print(highscore_word)
    print(max(scores))
    return {"score": max(scores), "high_extraction": highscore_word}
