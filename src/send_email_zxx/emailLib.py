# pylint: disable=invalid-name
# -*- encoding: utf-8 -*-
'''
@File        :   emailLib.py
@Time        :   2024/04/26 20:49:17
@Author      :   xiaoxian.zuo
@Email       :   zxx1980179070@163.com
@Description :   创建并发送邮件
'''

from abc import ABCMeta, abstractmethod
import ssl
import smtplib
from email.message import EmailMessage

# pylint: disable=too-few-public-methods
class SingleT:
    """单例模式"""
    # pylint: disable=unused-argument
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance


class MailBox(SingleT):
    """连接邮箱
    """
    context = ssl.create_default_context()
    def __init__(self, config):
        self.user = config.get("mail_user", "imap.qq.1980179070@qq.com")
        self.password = config.get("mail_pass", "wvdysnriotyzehgf")
        host = config.get("mail_host", "imap.qq.com")
        port = config.get("mail_port", 933)
        # 连接邮箱
        self.smtp = smtplib.SMTP(host=host, port=port)
        self.smtp.starttls(context=self.context)
        # 登录邮箱
        self.__login(self.user, self.password)

    def __login(self, user, password):
        self.smtp.login(user, password)
        print("=> login success")

    def logout(self):
        """退出邮箱登录
        """
        self.smtp.quit()
        print("=> logout success")


class SendEmailBuilder(metaclass=ABCMeta):
    """生成邮件 抽象接口
    """
    def __init__(self, **kwargs):
        # pylint: disable=invalid-name
        From = kwargs.get("From", None)
        To = kwargs.get("To", None)
        Subject = kwargs.get("Subject", None)
        Cc = kwargs.get("Cc", None)
        Body = kwargs.get("Body", None)
        Attachment = kwargs.get("Attachment", None)

        self.email = EmailMessage()
        self.email_from = From
        self.email_to = To
        self.email_subject = Subject
        self.email_cc = Cc
        self.email_body = Body
        self.email_attachment = Attachment

    @abstractmethod
    def generate_header(self):
        """生成邮件头"""
        # pylint: disable=pointless-statement
        # pylint: disable=unnecessary-pass
        pass

    @abstractmethod
    def gererate_body(self):
        """生成邮件体"""
        # pylint: disable=pointless-statement
        # pylint: disable=unnecessary-pass
        pass

    @abstractmethod
    def add_attachment(self):
        """添加邮件附件"""
        # pylint: disable=pointless-statement
        # pylint: disable=unnecessary-pass
        pass

    @abstractmethod
    def send_email(self):
        """ 发送邮件"""
        # pylint: disable=pointless-statement
        # pylint: disable=unnecessary-pass
        pass


def email_director(builder, mail_box):
    """ 规定生成邮件需要的步骤
    """
    builder.generate_header()
    builder.gererate_body()
    builder.add_attachment()
    builder.send_email()

    # 关闭 邮箱连接
    mail_box.logout()


class SendEmailAlert(SendEmailBuilder, SingleT):
    """ 生成具体的预警邮件, 并发送
    """
    def __init__(self, mail_box, **kwargs):
        super().__init__(**kwargs)
        self.smtp = mail_box.smtp

    def generate_header(self):
        """生成邮件头
        """
        self.email["From"] = self.email_from
        self.email["To"] = self.email_to
        self.email["Subject"] = self.email_subject
        if self.email_cc is not None:
            self.email["Cc"] = self.email_cc

    def gererate_body(self):
        """生成邮件体"""
        if self.email_body is not None:
            self.email.add_alternative(self.email_body, subtype='html')

    def add_attachment(self):
        """添加邮件附件"""
        attachment_list = self.email_attachment
        if attachment_list is not None:
            for attachment in attachment_list:
                path = attachment.get("path")
                filename = attachment.get("filename")
                maintype_subtype = attachment.get("maintype_subtype", "").split('/')
                maintype = maintype_subtype[0]
                subtype = maintype_subtype[1]
                with open(path, "rb") as file:
                    f_data = file.read()
                if maintype == "image":
                    self.email.add_attachment(f_data, maintype=maintype,
                                              subtype=subtype, filename=filename)
                else:
                    self.email.add_attachment(f_data, maintype=maintype,
                                              subtype=subtype, filename=filename)

    def send_email(self):
        """ 发送邮件"""
        if self.email_to is not None:
            self.smtp.send_message(self.email)
            print("=> send Email Alert success")
