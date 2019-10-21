"""
    消息填充模式
"""


class PKCS7Padding:
    """
    基于 PKCS7 的消息补位
    """

    BLOCK_SIZE = 32

    def encode(self, text: bytes) -> bytes:
        """"
        对需要加密的明文数据进行补位
        :param text: 明文数据
        :return: 补全的明文
        """
        text_length = len(text)
        amount_to_pad = self.BLOCK_SIZE - (text_length % self.BLOCK_SIZE)
        if amount_to_pad == 0:
            amount_to_pad = self.BLOCK_SIZE
        pad = chr(amount_to_pad)
        return text + (pad * amount_to_pad).encode()

    def decode(self, text_padded: bytes) -> bytes:
        """
        删除解密后的补位字符
        :param text_padded: 解密后的明文
        :return: 移除补位字符后的明文
        """
        pad = text_padded[-1]
        if pad < 1 or pad > self.BLOCK_SIZE:
            pad = 0
        return text_padded[:-pad]
