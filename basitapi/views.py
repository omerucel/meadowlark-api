#-*- coding: utf-8 -*-

from django.utils import simplejson
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, QueryDict

#from oauth2app.authorize import Authorizer, MissingRedirectURI, AuthorizationException

from basitapi.exception import ApiException
from basitapi.response import ApiResponse

"""
def oauth2_login(request):
    if request.user.is_authenticated == True:
        return HttpResponseRedirect('/oauth2/authorize')

    template_params = {}
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username,password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/oauth2/authorize')
            else:
                return HttpResponseRedirect('/oauth2/login')
        else:
            template_params['user_info_error'] = True

    template_params.update(csrf(request))

    return render_to_response('oauth2/login.html', template_params)

@login_required(login_url='/oauth2/login')
def missing_redirect_uri(request):
    return render_to_response('oauth2/missing_redirect_uri.html',{},RequestContext(request))

@login_required(login_url='/oauth2/login')
def authorize(request):
    authorizer = Authorizer()
    try:
        authorizer.validate(request)
    except MissingRedirectURI, e:
        return HttpResponseRedirect('/oauth2/missing_redirect_uri')
    except AuthorizationException, e:
        return authorizer.error_redirect()

    if request.method == 'GET':
        template_params = {
            'client' : authorizer.client,
            'access_ranges' : authorizer.access_ranges,
            'form_action' : '/oauth2/authorize?%s' % authorizer.query_string
        }
        template_params.update(csrf(request))

        return render_to_response('oauth2/authorize.html', template_params, RequestContext(request))
    elif request.method == 'POST':
        form = AuthorizeForm(request.POST)
        if form.is_valid():
            if request.POST.get('connect') == "Yes":
                return authorizer.grant_redirect()
            else:
                return authorizer.error_redirect()

    return HttpResponseRedirect('/')
"""

class ApiView(View):
    """
    View sınıflarına Api desteği kazandırır.
    """

    _format = None

    def http_method_not_allowed(self, request, *args, **kwargs):
        raise ApiException('Method not allowed.',405)

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        """
        Gelen istek application/x-www-form-urlencoded ile gönderilmişse
        raw_post_data içindeki veriler objeye çevrilir ve request.REQUEST güncellenir.
        """
        if request.META.get('CONTENT_TYPE') == 'application/x-www-form-urlencoded' and request.method in ['PUT']:
            request.REQUEST.dicts = (request.POST, request.GET, simplejson.loads(request.raw_post_data))

        try:
            # Yanıt formatını belirlemek için önce HTTP_ACCEPT kontrol ediliyor.
            if 'application/json' in request.META.get('HTTP_ACCEPT', ''):
                self._format = 'json'
            else:
                # Bağlantı son ekine göre format belirleniyor.
                self._format = kwargs.get('format', 'json')

                # Destek verilmeyen format isteklerinde hata görüntüle.
                if self._format not in ['json', 'xml']:
                    raise ApiException('Unsupported response format.', 400)

            # format parametrelerden temizleniyor. Boş yere kalabalık olmasın..
            if kwargs.has_key('format'):
                del kwargs['format']

            # method parametresi ile istek yapılırsa ilgili metodun çalıştırılması sağlanıyor. (method=PUT, method=POST vb.)
            # Diğer durumlar için View sınıfının dispatch metodu kullanılır.
            if request.REQUEST.get('method', '').lower() in self.http_method_names:
                handler = getattr(self, request.REQUEST.get('method').lower(), self.http_method_not_allowed)
            else:
                handler = super(ApiView, self).dispatch

            response = handler(request, *args, **kwargs)
        except ApiException, error:
            import traceback
            traceback.print_exc()
            data = {
                'message' : error.message,
                'status' : error.status
            }

            if not error.application_code == None:
                data.update({'application_code' : error.application_code})

            response = ApiResponse(data, error.status)
        except Exception, error:
            import traceback
            traceback.print_exc()
            response = ApiResponse({
                'message' : 'Internal Server Error',
                'status' : 500
            }, 500)
        finally:
            # TODO : Yanıtın farklı formatlarda sunulabilmesini destekle
            if isinstance(response, ApiResponse):
                status_code = response.status
                mimetype = 'text/plain'
                if self._format == 'json':
                    mimetype = 'application/json'
                elif self._format == 'xml':
                    mimetype = 'text/xml'

                response = HttpResponse(response.to_json(), '%s; charset=utf-8' %(mimetype))
                response.status_code = status_code

            # İstemci tarafındaki yetersizliklerden dolayı bazen 200 haricindeki hata kodları soruna neden olabiliyor.
            # Bu sorunu aşmak için suppress_response_codes=1 değeri ile istekte bulunmak yeterli.
            if request.GET.get('suppress_response_codes', False) == '1':
                response.status_code = 200

            return response

