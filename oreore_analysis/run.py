from flask import Flask, render_template, url_for, request, redirect, Blueprint
import os
import controllers


app = controllers.app


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8888))
    app.debug = True  # デバッグモード有効化
    app.run(host="0.0.0.0", port=port)