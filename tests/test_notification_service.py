from app.notifications.notiication_service import (
    EmailNotificationService,
    SMSNotificationService,
)


def test_email_notification(capsys):
    service = EmailNotificationService()

    service.send_notification("Student created")

    captured = capsys.readouterr()

    assert captured.out == "Email Notification : Student created\n"


def test_sms_notification(capsys):
    service = SMSNotificationService()

    service.send_notification("Student created")

    captured = capsys.readouterr()

    assert captured.out == "SMS Notification : Student created\n"
