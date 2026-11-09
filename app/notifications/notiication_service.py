from abc import ABC, abstractmethod


class NotificationService(ABC):
    @abstractmethod
    def send_notification(self, message: str):
        pass


class EmailNotificationService(NotificationService):
    def send_notification(self, message):
        print(f"Email Notification : {message}")


class SMSNotificationService(NotificationService):
    def send_notification(self, message):
        print(f"SMS Notification : {message}")
