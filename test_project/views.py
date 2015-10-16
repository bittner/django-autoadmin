from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .literals import TEST_MOCK_VIEW_TEXT


@login_required
def mock_view(request):
    return HttpResponse(TEST_MOCK_VIEW_TEXT)
