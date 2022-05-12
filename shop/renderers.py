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
                "data": {"id": data["id"], "message": "Product added"}
            }
        elif renderer_context['request'].method == 'DELETE':
            response = {
                "data": {"id": data["id"], "message": "Product deleted"}
            }
        elif renderer_context['request'].method == 'PATCH':
            response = {"data": data}
        return super(CustomRenderer, self).render(response, accepted_media_type, renderer_context)


class CartRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, render_context=None):
        if render_context['request'].method == 'DELETE':
            response = {
                "data": {"message": "Item removed from cart"}
            }
            render_context['response'].status_code = 200
        elif render_context['request'].method == 'POST':
            response = {
                "data": {"message": "Product add to card"}
            }
        elif render_context['request'].method == 'GET':
            response = {"data": data}
        return super(CartRenderer, self).render(response, accepted_media_type, render_context)


class OrderRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, render_context=None):
        if render_context['request'].method == 'GET':
            for product in data:
                del product['user']
            response = {"data": data}
        elif render_context['request'].method == 'POST':
            response = {"data": {"order_id": data['id'], "message": "Order is prodded"}}
        return super(OrderRenderer, self).render(response, accepted_media_type, render_context)
