from flask import Flask, render_template, url_for, request, redirect, Blueprint
import os
import controllers


from os.path import join, dirname
from dotenv import load_dotenv

app = controllers.app


load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

LINE_TOKEN = os.environ.get("LINE_TOKEN")


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8888))
    app.debug = True  # デバッグモード有効化
    app.run(host="0.0.0.0", port=port)