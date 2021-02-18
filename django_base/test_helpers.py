from django.http.response import HttpResponse


class TestHelpers:
    @staticmethod
    def assert_message(response: HttpResponse, message: str) -> None:
        messages = [m.message for m in response.context['messages']]
        if message not in messages:
            raise AssertionError(f"{message} not found in {messages}")

    @staticmethod
    def assert_content(response: HttpResponse, text: str) -> None:
        body = response.content.decode('utf-8')
        if text not in body:
            raise AssertionError(f"{text} not found in response body")

    @staticmethod
    def assert_no_content(response: HttpResponse, text: str) -> None:
        body = response.content.decode('utf-8')
        if text in body:
            raise AssertionError(f"body contains {text}")
