# AudioBible

King James Version Audio Bible and Text Download Spider


#### How to use

    # download this project with git clone
    git clone https://github.com/gxela/AudioBible
    cd AudioBible/
    
    # install scrapy
    pip install -r requirements.txt
    
    cd kjv/
    
    # run this command to download the text and audio
    scrapy crawl bible
    

#### For developers: How to create a spider with Python Scrapy that will download KJV Bible audio book mp3 and text

    # create a VirtualEnv
    virtualenv Python2
    
    # activate the virtualenv
    . Python2/bin/activate
    
    # install scraping engine
    pip install scrapy
    
    # create a scrapy project and generate the spider, then paste the files included with this gist into the project
    scrapy startproject kjv audiobible
    cd audiobible
    scrapy genspider bible www.audiobible.com

    # now copy and paste all the files, then run the commands below to fist download all the books and chapters and urls, 
    #  then to actually download the mp3 file and text, run the command twice
    scrapy crawl bible
    
    scrapy crawl bible  # download the urls, when run for the first time
    scrapy crawl bible  # save the mp3 and text files, when urls exist, since it was ran the first time
    
    # now if you look you will see all the data places into the bible/ directory, have fun and PRAISE THE LORD JESUS CHRIST!
    ls bible/
