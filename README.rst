Python WorkWeiXin

A Python wrapper around for Work WeiXin API.

.. image:: https://travis-ci.org/sns-sdks/python-workweixin.svg?branch=master
    :target: https://travis-ci.org/sns-sdks/python-workweixin
    :alt: Build Status

.. image:: https://codecov.io/gh/sns-sdks/python-workweixin/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/sns-sdks/python-workweixin
    :alt: Codecov


Introduction
============

This library provide easy method to use `work.weixin <https://work.weixin.qq.com/>`_ apis.

Using
=====

Message
-------

Now you can use this library to `send message <https://work.weixin.qq.com/api/doc#90000/90135/90235>`_ in work.weixin app.

This exposed with ``work.Api`` class.

You can create an instance of this api to begin::


    In [1]: from pywework.api.work import Api

    In [2]: api = Api(corp_id='your work id', corp_secret='your work secret', agent_id='')

Now you can send message to user::

    In [6]: api.send_text('Hello', to_user='liukun')
    Out[6]: {'errcode': 0, 'errmsg': 'ok', 'invaliduser': ''}


TODO
====
