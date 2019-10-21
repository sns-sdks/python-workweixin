"""
    Tests for pywework.crypto modules
"""
import base64
import unittest

from pywework.crypto.msg_crypto import MsgCrypto
from pywework.crypto.padding import PKCS7Padding
from pywework.crypto.sign import get_sha1_signature
from pywework.crypto.validation import MessageValidation
from pywework.error import WeWorkError
from pywework.message.xml import xml_message


class CryptoTest(unittest.TestCase):
    def setUp(self) -> None:
        self.token = "hJqcu3uJ9Tn2gXPmxx2w9kkCkCE2EPYo"
        self.aes_key = "6qkdMrq68nTKduznJYO1A37W2oEgpkMUvkttRToqhUt"
        self.receive_id = "ww1436e0e65a779aee"

    def testMsgCrypto(self) -> None:
        with self.assertRaises(ValueError):
            m = MsgCrypto(b"aes_key")
            m.encipher("hello", self.receive_id)

        key = base64.b64decode(self.aes_key + "=")
        msg_crypto = MsgCrypto(key)

        data = "hello"
        st, cipher_text = msg_crypto.encipher(data, self.receive_id)
        self.assertEqual(st, 0)

        st, plain_text = msg_crypto.decipher(cipher_text, self.receive_id)
        self.assertEqual(st, 0)
        self.assertEqual(data, plain_text)

        self.assertEqual(16, len(msg_crypto.get_random_str()))

    def testPadding(self) -> None:
        padding = PKCS7Padding()
        data = b"zBo7AYstNVlZaCq2TirxRS5dFEcOk8gQ"
        en_padding = padding.encode(data)
        remove_padding = padding.decode(en_padding)
        self.assertEqual(data, remove_padding)

    def testGetSign(self) -> None:
        st, sign = get_sha1_signature("token", "12345", "string", "encrypt")
        self.assertEqual(st, 0)

        st, sign = get_sha1_signature("token", ["12345"], "string", "encrypt")
        self.assertNotEqual(st, 0)

    def testValidation(self) -> None:
        with self.assertRaises(WeWorkError):
            MessageValidation(
                token=self.token, aes_key="aes_key", receive_id=self.receive_id
            )

        m = MessageValidation(
            token=self.token, aes_key=self.aes_key, receive_id=self.receive_id
        )

        st, echo_str = m.verify_url(
            signature="012bc692d0a58dd4b10f8dfe5c4ac00ae211ebeb",
            timestamp="1476416373",
            nonce="47744683",
            echo_str="fsi1xnbH4yQh0+PJxcOdhhK6TDXkjMyhEPA7xB2TGz6b+g7xyAbEkRxN/3cNXW9qdqjnoVzEtpbhnFyq6SVHyA==",
        )
        self.assertEqual(st, 0)
        self.assertEqual(echo_str, "1288432023552776189")

        data = "hello"
        st, send_data = m.msg_build(
            reply=data, nonce="12345678", timestamp="1476416373"
        )
        self.assertEqual(st, 0)

        sign = xml_message.parse_message(message=send_data, respond=True)[
            "MsgSignature"
        ]

        st, res = m.msg_parse(
            msg=send_data, signature=sign, timestamp="1476416373", nonce="12345678"
        )
        self.assertEqual(st, 0)
        self.assertEqual(res, data)
