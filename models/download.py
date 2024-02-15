from pytube import YouTube


def uvid_downlaod(url,path,filename) :
    yt = YouTube(url)
    try:
        yt.streams.filter(progressive = True, 
    file_extension = "mp4").first().download(output_path = "./Static_files/Youtube/", 
    filename = filename)
    except:
        print("Some Error!")
    print('Task Completed!')