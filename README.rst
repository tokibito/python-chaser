=============
python-chaser
=============

|build-status| |pypi|

CHaser client for Python

ライブラリの利用
================

PyPIにアップロードしているので、インストールにはpipコマンドを使えます。

::

   (venv)$ pip install chaser

使い方は、 `example/simple.py` `example/mapper.py` を参考にしてみてください。

ライブラリの開発
================

ライブラリ開発で利用する依存モジュールはpipでインストールできます。

::

   $ pip install -e .[dev]

.. |build-status| image:: https://travis-ci.org/tokibito/python-chaser.svg?branch=master
   :target: https://travis-ci.org/tokibito/python-chaser
.. |pypi| image:: https://badge.fury.io/py/chaser.svg
   :target: http://badge.fury.io/py/chaser
