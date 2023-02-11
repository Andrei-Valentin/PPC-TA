import warnings

from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import ListView

from .Metadata import get_metadata
from .forms import DocumentForm
from .models import Document
from .predict import predict_gen

warnings.simplefilter('ignore')


class IndexView(ListView):
    template_name = 'music/index.html'

    def get_queryset(self):
        return True


def model_form_upload(request):
    documents = Document.objects.all()
    if request.method == 'POST':
        if len(request.FILES) == 0:
            messages.error(request, 'Upload a file')
            return redirect("predictor:index")

        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            upload_file = request.FILES['document']
            if not upload_file.name.endswith('.wav'):
                messages.error(request, 'Only .wav file type is allowed')
                return redirect("predictor:index")
            meta = get_metadata(upload_file)

            genre = predict_gen(meta)

            context = {'genre': genre}
            return render(request, 'music/result.html', context)

    else:
        form = DocumentForm()

    return render(request, 'music/result.html', {'documents': documents, 'form': form})
