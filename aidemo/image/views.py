from django.shortcuts import render, redirect
from .forms import SegmentForm
from .models import SegmentModel
# Create your views here.
from utils.evaluation import evaluate
import random, string
from django.views.decorators.csrf import csrf_exempt
# create a view with post and get request

@csrf_exempt
def index(request):

    if request.method == 'POST':
        # do something
        form = SegmentForm(request.POST, request.FILES)
        # print(form)
        if form.is_valid():
            instance = form.save()
            content_file, output = evaluate(instance.inputFile.path, instance.type)
            path_name = ''
            try:
                path_name = instance.inputFile.name.split('/')[1].split('.')[0]
            except:
                path_name = ''.join(random.choices(string.ascii_lowercase, k=9))

            instance.outputFile.save("output_" + path_name +'.png', content_file)
            instance.maskedFile.save("masked_" + path_name +'.tif', output)
            instance.save()
            return redirect('output', pk=instance.pk)
            # return render(request, 'output.html', {'image': instance.outputFile})
        else:
            print(form.errors)
        
        return render(request, 'index.html', {'form': form})
    elif request.method == 'GET':
        form = SegmentForm()
        return render(request, 'index.html', {'form': form})


def output(request, pk):

    instance = SegmentModel.objects.get(pk=pk)

    return render(request, 'output.html', context={'image': instance.outputFile, 'instance' : instance})



import os
# Import HttpResponse module
from django.http.response import HttpResponse
import os
import magic

def download_file(request, pk):
    image = SegmentModel.objects.get(pk=pk)
    # image = ImageModel.objects.get(pk=self.kwargs['image_id'])
    image_buffer = open(image.maskedFile.path, "rb").read()
    content_type = magic.from_buffer(image_buffer, mime=True)
    response = HttpResponse(image_buffer, content_type=content_type);
    response['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(image.maskedFile.path)
    return response
