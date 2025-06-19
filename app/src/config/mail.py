from fastapi_mail import FastMail, MessageSchema,ConnectionConfig

conf = ConnectionConfig(
    MAIL_USERNAME = "rra@ecomp.poli.br",
    MAIL_PASSWORD = "Soenten!23",
    MAIL_FROM = "rra@ecomp.poli.br",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_FROM_NAME="Suporte App-Cancer",
    MAIL_TLS = True,
    MAIL_SSL = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

def email_html(email, token,adress):
    html = """
    Entre no link para resetar sua senha <a href="{}/auth/reset-password/?email={}&token_reset_password={}">Link</a>
    """.format(adress,email, token)
    return html


async def simple_send(email,token,adress):
    message = MessageSchema(
        subject="Fastapi-Mail",
        recipients=[email],  # List of recipients, as many as you can pass
        body=email_html(email, token,adress),
        subtype="html"
        )

    fm = FastMail(conf)
    await fm.send_message(message)
    return {"message": "email has been sent"}
