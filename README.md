# EmailLib

**EmailLib** 简单的连接邮箱, 生成邮件并发送.


```python
from send_email_zxx.emailLib import MailBox, SendEmailAlert, email_director

config = {
    "mail_port": 587,
    "mail_host": "smtp.qq.com",
    "mail_user": "user", # 邮箱用户名
    "mail_pass": "", # 授权码
}
message = {
    "Subject": "Test ...",                 # 主题   必填
    "Body": "<h1>test send email</h1>",    # 正文   必填
    "To": "xxxxx@qq.com,xxxxx@qq.com",     # 接收人 必填
    "Cc": "xxxxx@qq.com,xxxxx@qq.com",     # 抄送人 可选
    "From": "xxxxx@qq.com",                # 发送人 必填
    "Attachment": [                        # 附件 可选
        {
            "path": "文件完整路径",
            "filename": "文件名称",
            "maintype_subtype": "maintype/subtype"
        }
    ]
}
# 连接邮箱
mail_box=MailBox(config)

# 生成邮件
email_alert = SendEmailAlert(mail_box, **message)

# 发送邮件
email_director(email_alert, mail_box)
```