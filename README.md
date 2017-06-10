# AudioBible

King James Version Audio Bible

**Note:** This project is not associated with AudioBible.com, please purchase a KJV Bible from [audiobible.com](http://audiobible.com/kjv-audio-bible-king-james/) if you like this.

- [King James Audio Bible Download for MP3 and iPod devices](http://www.audiobible.com/king-james-bible-download-for-mp3-and-ipod/)
- [Russian Audio Bible Download for MP3 or iPod devices](http://www.audiobible.com/download-russian-audio-bible-mp3-and-ipod/)
- [Mandarin Chinese Audio Bible Download for MP3, iPhone or iPod](http://www.audiobible.com/mandarin-chinese-audio-bible-download-mp3-ipod-devices/)

## How to use

    pip install audiobible                      # install AudioBible with python pip
    
    audiobible init                             # download data about all books and chapters in the KJV
    audiobible load                             # download all books' and chapters' text and audio mp3 files

    audiobible list                             # to list all books and the number of chapters each book has

    audiobible hear                             # to hear the book of "Genesis" chapter 1
    audiobible hear mark                        # to hear the book of "Mark" chapter 1
    audiobible hear -b mark                     # to hear the book of "Mark" chapter 1
    audiobible hear mark 4                      # to hear the book of "Mark" chapter 4
    audiobible hear -b mark -c 4                # to hear the book of "Mark" chapter 4
    audiobible hear 1_john 3                    # to hear the book of "1 John" chapter 3
    audiobible hear -b 1_john -c 3              # to hear the book of "1 John" chapter 3
    
    audiobible read mark 4                      # to read Mark 4, (use params like with hear operation)
    
    audiobible find                             # to output the whole bible, a whole book or a whole chapter
    audiobible find water of life               # to find water of life, say words to search for as params
    audiobible find water                       # to find water, say the word to search the whole bible
    audiobible find 'circle of the earth'       # to find circle of the earth, say the words to search of as a string
    audiobible find circle                      # or find the same results with just looking for circle
    
    audiobible find jesus -b luke -c 3 -C 2     # to find jesus in the book of "Luke" chapter 3, showing 2 verses before and after the matched verse context (use `-A` or `-B` to show before or after context only)
    

# KJV Bible - List of Books and Chapters Count

**Note:** This list can be shown by typing `audiobible list`

    Old Testament                 |   ###   | New Testament                 |   ##
    ------------------------------|---------|-------------------------------|--------
    GENESIS                       |   50    | MATTHEW                       |   28
    EXODUS                        |   40    | MARK                          |   16
    LEVITICUS                     |   27    | LUKE                          |   24
    NUMBERS                       |   36    | JOHN                          |   21
    DEUTERONOMY                   |   34    | ACTS                          |   28
    JOSHUA                        |   24    | ROMANS                        |   16
    JUDGES                        |   21    | 1_CORINTHIANS                 |   16
    RUTH                          |   4     | 2_CORINTHIANS                 |   13
    1_SAMUEL                      |   31    | GALATIANS                     |   6
    2_SAMUEL                      |   24    | EPHESIANS                     |   6
    1_KINGS                       |   22    | PHILIPPIANS                   |   4
    2_KINGS                       |   25    | COLOSSIANS                    |   4
    1_CHRONICLES                  |   29    | 1_THESSALONIANS               |   5
    2_CHRONICLES                  |   36    | 2_THESSALONIANS               |   3
    EZRA                          |   10    | 1_TIMOTHY                     |   6
    NEHEMIAH                      |   13    | 2_TIMOTHY                     |   4
    ESTHER                        |   10    | TITUS                         |   3
    JOB                           |   42    | PHILEMON                      |   1
    PSALMS                        |   150   | HEBREWS                       |   13
    PROVERBS                      |   31    | JAMES                         |   5
    ECCLESIASTES                  |   12    | 1_PETER                       |   5
    SONG_OF_SOLOMON               |   8     | 2_PETER                       |   3
    ISAIAH                        |   66    | 1_JOHN                        |   5
    JEREMIAH                      |   52    | 2_JOHN                        |   1
    LAMENTATIONS                  |   5     | 3_JOHN                        |   1
    EZEKIEL                       |   48    | JUDE                          |   1
    DANIEL                        |   12    | REVELATION                    |   22
 
 