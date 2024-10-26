from django.http import HttpResponse
from django.shortcuts import redirect, render

from image_compression.forms import CompressImageForm
from PIL import Image
import io


def compress(request):
    user = request.user
    if request.method == 'POST':
        form = CompressImageForm(request.POST, request.FILES)
        if form.is_valid():
            original_img = form.cleaned_data['original_img']
            quality = form.cleaned_data['quality']
            
            compressed_image = form.save(commit=False)
            compressed_image.user = user
            
            # Perform Compression
            img = Image.open(original_img)
            output_format = img.format
            # buffer is to store the image binary data
            # we are trying to create a container for storing the compressed image
            buffer = io.BytesIO()
            # print('buffer===>', buffer) #  <_io.BytesIO object at 0x0000018EC6B1BF60>
            # print('buffer===>', buffer.getvalue()) # buffer===> b'' it is empty at this stage
            img.save(buffer, format=output_format, quality=quality)
            
            buffer.seek(0) # set the buffer cursor possition to 0
            # print('buffer===>', buffer.getvalue()) # The buffer will contain the hex decimal data of the compressed image
            
            # Save the compressed image inside the model
            compressed_image.compressed_img.save(
                f'compressed_{original_img}', buffer
            )
            
            # Automatically download the compressed file
            response = HttpResponse(buffer.getvalue(), content_type=f'image/{output_format.lower()}')
            response['Content-Disposition'] = f'attachment; filename=compressed_{original_img}'
            
            return response
       
    else:
        form = CompressImageForm()
        
        context = {
            'form': form
        }
        return render(request, 'image_compression/compress.html', context)
        

