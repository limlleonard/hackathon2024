import os
import pypandoc
pypandoc.download_pandoc()

dir1='/home/ll/Downloads/knowledgefilesforresearcher'
for file1 in os.listdir(dir1):
    dir_md=os.path.join(dir1, file1)
    dir_pdf=dir_md[:-2]+'pdf'
    # print(dir_md, dir_pdf)
    output = pypandoc.convert_file(dir_md, "pdf", outputfile=dir_pdf)
    assert output == ""



# dir_pdf='./files'
# embeder1=Embeder(dir_pdf)
# api1=os.getenv('openai_api')
# embeder1.init_llama(api1)
# embeder1.embed()
# frg1='what is the topic of the pdf file?'
# ant1=embeder1.qa(frg1)
# print(ant1)