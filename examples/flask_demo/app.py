"""
    Flask Demo App
"""
import time

from flask import Flask, request, make_response, jsonify

from .ext import wework, wework_msg_validation, wework_msg_xml_parser

app = Flask(__name__)


@app.route('/wework', methods=['GET', 'POST'])
def hello():
    if request.method == 'GET':
        r_sign = request.args.get('msg_signature')
        r_timestamp = request.args.get('timestamp')
        r_nonce = request.args.get('nonce')
        r_echo_str = request.args.get('echostr')

        ret, reply_str = wework_msg_validation.verify_url(
            r_sign, r_timestamp, r_nonce, r_echo_str
        )
        if ret != 0:
            print("ERR: VerifyURL ret: " + str(ret))
            return make_response(jsonify({"msg": "error"}))
        return make_response(reply_str)
    elif request.method == 'POST':
        r_sign = request.args.get('msg_signature')
        r_timestamp = request.args.get('timestamp')
        r_nonce = request.args.get('nonce')
        r_xml_data = request.data.decode('utf-8')

        ret, content = wework_msg_validation.msg_parse(
            r_xml_data, r_sign, r_timestamp, r_nonce
        )

        if ret != 0:
            print("ERR: Decrypt error. ret: " + str(ret))
            return make_response(jsonify({"msg": "error"}))

        recv_info = wework_msg_xml_parser.parse_message(content)
        print(recv_info)

        send_info = wework_msg_xml_parser.build_message(
            'text', ToUserName='xx', FromUserName='xx',
            CreateTime=time.time(), Content='World',
            MsgId=1234567890123456, AgentID=wework.agent_id
        )
        ret, con = wework_msg_validation.msg_build(
            send_info, r_nonce, r_timestamp
        )
        print(con)
        if ret != 0:
            print("ERR: Encrypt error. ret: " + str(ret))
            return make_response(jsonify({"msg": "error"}))
        return make_response(con)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6001)
