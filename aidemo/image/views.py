from django.shortcuts import render, redirect
from .forms import SegmentForm
from .models import SegmentModel
# Create your views here.
from utils.evaluation import evaluate
import random, string
# create a view with post and get request
def index(request):

    if request.method == 'POST':
        # do something
        form = SegmentForm(request.POST, request.FILES)
        # print(form)
        if form.is_valid():
            instance = form.save()
            content_file = evaluate(instance.inputFile.path)
            path_name = ''
            try:
                path_name = instance.inputFile.name.split('/')[1].split('.')[0]
            except:
                path_name = ''.join(random.choices(string.ascii_lowercase, k=9))

            instance.outputFile.save("output_" + path_name +'.png', content_file)
            instance.save()
            print('heeloo')
            return redirect('output', pk=instance.pk)
            # return render(request, 'output.html', {'image': instance.outputFile})
        else:
            print(form.errors)
        
        return render(request, 'index.html')
    elif request.method == 'GET':
        form = SegmentForm()
        return render(request, 'index.html', {'form': form})


def output(request, pk):

    instance = SegmentModel.objects.get(pk=pk)

    return render(request, 'output.html', context={'image': instance.outputFile})