from rest_framework import mixins
from rest_framework.renderers import BaseRenderer
from rest_framework.response import Response as DrfResponse
from rest_framework.utils import json
from rest_framework.viewsets import GenericViewSet


class Response(DrfResponse):

    def __init__(self, data=None, message=None, status=None,
                 template_name=None, headers=None,
                 exception=False, content_type=None):
        data_content = {
            'status': status,
            'data': data,
            'message': message,
        }
        super(Response, self).__init__(
            data=data_content,
            status=status,
            template_name=template_name,
            headers=headers,
            exception=exception,
            content_type=content_type
        )


class ApiRenderer(BaseRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response_dict = {
            'status': 'success',
            'data': {},
            'message': '',
        }
        response_dict['data'] = {"data": data}
        data = response_dict
        return json.dumps(data)


class CstmGenericViewSet(GenericViewSet):
    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)
        print(response)
        response_dict = {
            'status': response.status_code,
            'data': response.data,
        }
        # Modify the response object here
        response.data = response_dict

        return response


class CstmModelViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    CstmGenericViewSet,
):
    pass
