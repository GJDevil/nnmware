# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.db.models.query_utils import Q
from nnmware.apps.shop.models import Product
from nnmware.core.ajax import AjaxLazyAnswer, AjaxAnswer
from nnmware.core.imgutil import make_thumbnail


def autocomplete_search(request,size=16):
    results = []
    search_qs = Product.objects.filter(
        Q(name__icontains=request.REQUEST['q']) |
        Q(name_en__icontains=request.REQUEST['q'])).order_by('name')[:5]
    for r in search_qs:
        img = make_thumbnail(r.main_image,width=size)
        userstring = {'name': r.name, 'path': r.get_absolute_url(),
                      'img': img,
                      'slug': r.slug, 'amount':"%0.2f" % (r.amount,) }
        results.append(userstring)
    payload = {'answer': results}
    return AjaxLazyAnswer(payload)