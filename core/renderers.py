from rest_framework.renderers import JSONRenderer


class StandardResponseRenderer(JSONRenderer):
    """Format API responses in a standard way"""
    
    def render(self, data, accepted_media_type=None, renderer_context=None):
        """Render successful responses with consistent format"""
        response = renderer_context.get('response')

        # Format success responses
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