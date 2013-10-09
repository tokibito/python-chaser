# coding: utf-8
from setuptools import setup, find_packages

DOC = """
================
nullpobug.chaser
================

動作環境
========

* Python2.7

インストール
============

easy_installやpipでインストールしてください。

::

   $ pip install nullpobug.chaser

簡単な使い方
============

動かずサーチだけ実行するCHaserクラスを作ってみます。

**my_chaser.py**:

::

   from nullpochaser.chasers.silent import SilentCHaser

   class MyCHaser(SilentCHaser):
       pass

これを動かすには次のようにコマンドを実行します。

::

   $ python -m nullpochaser.main --chaser=my_chaser.MyCHaser

``-p`` オプションでポート番号を指定できます。他のオプションを確認するには、 ``--help`` オプションを指定してください。

::

   $ python -m nullpochaser.main --help

詳しくはソースを読んでください。
"""

setup(
    name='nullpobug.chaser',
    version='0.1',
    description='CHaser 2012 client library for Python',
    long_description=DOC,
    author='Shinya Okano',
    classifiers=[
        'Programming Language :: Python :: 2.7',
    ],
    packages=find_packages(),
)
