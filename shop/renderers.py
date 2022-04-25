from rest_framework.renderers import JSONRenderer


class CustomRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = data
        if renderer_context['request'].method == 'GET':
            response = {
                "data": data,
            }
        elif renderer_context['request'].method == 'POST':
            response = {
                "data": {"id": data.id, "message": "Product added"}
            }
        elif renderer_context['request'].method == 'DEL':
            response = {
                "data": {"id": data.id, "message": "Product deleted"}
            }
        return super(CustomRenderer, self).render(response, accepted_media_type, renderer_context)
