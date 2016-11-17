def handle_uploaded_file(f):
     with open(r't.txt', 'wb+') as fr:
        for line in f.chunks():
           fr.write(line)
 #   for line in f.chunks():
        
