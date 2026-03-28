from rest_framework.renderers import JSONRenderer


class StandardResponseRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context.get('response')

        if response and 200 <= response.status_code < 300:

            message = "Success"
            if isinstance(data, dict):
                message = data.pop('message', 'Success')

            standard_response = {
                "isSuccess": True,
                "message": message,
                "data": data
            }
            return super().render(standard_response, accepted_media_type, renderer_context)

        return super().render(data, accepted_media_type, renderer_context)