from flask import Flask, request, Blueprint, jsonify
import speech_recognition as sr
import os
import MeCab
import json
from gensim.models import word2vec
from gensim.models import KeyedVectors
import requests


# Blueprintオブジェクトを生成
app = Blueprint('input_data', __name__)

model = KeyedVectors.load_word2vec_format('apps/word_model/entity_vector.model.bin', binary=True)
# model = KeyedVectors.load_word2vec_format('apps/word_model/entity_vector.model.bin')
# tagger = MeCab.Tagger("-d /var/lib/mecab/dic/ipadic")
tagger = MeCab.Tagger("-d /usr/local/lib/mecab/dic/ipadic/")
tagger.parse("")

open("./scam_info.json", 'w')

@app.route('/scam_check', methods=['POST'])
def input_data():
    if 'file' not in request.files:
        return "ファイル未指定"
    fs = request.files['file']
    
    # ファイルを保存
    save_path = f"upload/{fs.filename}"
    fs.save(save_path)

    audio_recognized = voice_recognize(save_path)
    print(audio_recognized)
    if audio_recognized is None:
        return jsonify({"msg": "fail"})
        
    scam_result =  scam_check(audio_recognized)
    # return jsonify(scam_result)
    return jsonify({"msg":"sucess", "content": scam_result})

# 現在のスコアを取得する
@app.route("/current_score", methods=['GET'])
def current_score():
    with open("./scam_info.json", 'r') as outfile:
        # json.dump(scam_infomation, outfile, ensure_ascii=False)
        json_data = json.load(outfile)
    
    # return jsonify({"total_score": json_data["threat_score"], "result": json_data["results"]})
    return jsonify(json_data)

def voice_recognize(save_path):
    print("音声認識を開始します") 
    r = sr.Recognizer()
    with sr.AudioFile(save_path) as source:
        audio = r.record(source)

    try:
        result_recognized = r.recognize_google(audio, language='ja-JP')
    except sr.UnknownValueError:
        print("音声認識ができませんでした")
        return None
    return result_recognized

# 特殊詐欺を検知する
def scam_check(text):
    #渡されたテキストを形態素解析
    node = tagger.parseToNode(text)
    scores = []
    results = []
    # 特殊詐欺に使われそうな語群
    # keywords = ['金', '振込', '急用', 'ATM', '銀行']
    keywords = ["泡", "石鹸", "シャンプー"]
    while node is not None:
        fields = node.feature.split(",")
        if fields[0] == '名詞' or fields[0] == '動詞' or fields[0] == '形容詞':    
            try:
                for keyword in keywords:
                    #　単語とkeywordの類似度
                    similarity_score = model.wv.similarity(node.surface, keyword)
                    if similarity_score >= 0.6:
                        scores.append(similarity_score)
                        results.append(
                            {"similarity_score": float(similarity_score), "trigger_keyword": str(keyword), "target_keyword": str(node.surface)}
                        )
            # 学習modelに切り取った言葉がない例外処理
            except KeyError:
                pass 
        node = node.next
    
    try:
    # 類似度数のリストの平均を脅威度としている
        threat_score = sum(scores) / len(scores)
    except ZeroDivisionError:
        print("scoresのlengthがゼロになったので、単語に対する脅威度を出さない")
        threat_score = 0
        pass
    # print(scores)
    # threat_score = sum(scores)

    with open("./scam_info.json", 'r') as outfile:
        try:
            json_data = json.load(outfile)
            total_score = json_data["total_score"]
            if total_score >= 10:
                send_line_notify("この通話はオレオレ詐欺の可能性があります。")

        except json.decoder.JSONDecodeError:
            total_score = 0
        
    
    total_score += threat_score
    scam_infomation = {"total_score": total_score, "threat_score": threat_score, "results": results}
    
    with open("./scam_info.json", 'w') as outfile:
        json.dump(scam_infomation, outfile, ensure_ascii=False)
    
    return scam_infomation

def send_line_notify(notification_message):
    line_notify_token = os.environ.get("LINE_TOKEN")
    line_notify_api = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': f'Bearer {line_notify_token}'}
    data = {'message': f'message: {notification_message}'}
    requests.post(line_notify_api, headers = headers, data = data)