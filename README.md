# AudioBible

## King James Version Audio Bible for Mac, Windows and Unix/Linux


# Install On Mac

    brew install python libxml2                                 # install dependencies
    pip install scrapy
    pip install audiobible                                      # install AudioBible with python pip


# Install On Ubuntu Linux

    sudo apt-get install python-pip libxml2 python-lxml         # install dependencies
    sudo pip install scrapy
    sudo pip install audiobible                                 # install AudioBible with python pip


# How to use

    pip install --upgrade audiobible                            # update AudioBible to the latest version

    audiobible update                                           # update AudioBible using pip command internally
    
    audiobible -h | --help                                      # show help
    audiobible help                                             # show help
    
    audiobible version                                          # show version number and exit
    
    audiobible init                                             # download data about all books and chapters in the KJV
    
    audiobible load                                             # download all books' and chapters' text and audio mp3 files
    
    audiobible list                                             # to list all books and the number of chapters each book has
    
    audiobible praise                                           # open a browser to a youtube playlist with hymns for praising God
    
    audiobible path daniel                                      # show the path on the hard drive to the book of "Daniel"
    
    audiobible quote                                            # to output a quote
    
    audiobible hear mark                                        # to hear the book of "Mark" chapter 1
    audiobible hear -b mark                                     # to hear the book of "Mark" chapter 1
    audiobible hear mark 4                                      # to hear the book of "Mark" chapter 4
    audiobible hear -b mark -c 4                                # to hear the book of "Mark" chapter 4
    audiobible hear 1_john 3                                    # to hear the book of "1 John" chapter 3
    audiobible hear -b 1_john -c 3                              # to hear the book of "1 John" chapter 3
    
    audiobible read mark 4                                      # to read Mark 4, (use params like with hear operation)
    
    audiobible show mark 4                                      # to show the book of "Mark" chapter 4 text in the terminal
    
    audiobible find                                             # to output the whole Bible
    audiobible find -b 2_john                                   # to output the whole book of "2 John"
    audiobible find -b james -c 5                               # to output chapter 5 for the book of "James"
    audiobible find water of life                               # to find water of life, say words to search for as params
    audiobible find water                                       # to find water, say the word to search the whole bible
    audiobible find 'it is done'                                # to find it is done, say the words to search as a string
    audiobible find circle of the earth                         # to find circle of the earth
    
    audiobible find jesus -b luke -c 3 -C 2                     # to find jesus in the book of "Luke" chapter 3, showing 2 verses before and after the matched verse context
    audiobible find circle -A 5 -B 2                            # to show 2 verse before and 5 verses after the matched verse context

    audiobible quote                                            # usage is same as with find operation


**Note:** Tested and created on a Mac, should work on Windows and Unix/Linux and other OSes.

**Note:** This project is not associated with AudioBible.com, please purchase a KJV Bible from [audiobible.com](http://audiobible.com/kjv-audio-bible-king-james/) if you like this.

- [King James Audio Bible Download for MP3 and iPod devices](http://www.audiobible.com/king-james-bible-download-for-mp3-and-ipod/)
- [Russian Audio Bible Download for MP3 or iPod devices](http://www.audiobible.com/download-russian-audio-bible-mp3-and-ipod/)
- [Mandarin Chinese Audio Bible Download for MP3, iPhone or iPod](http://www.audiobible.com/mandarin-chinese-audio-bible-download-mp3-ipod-devices/)


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
    HOSEA                         |   14    |
    JOEL                          |   3     |
    AMOS                          |   9     |
    OBADIAH                       |   1     |
    JONAH                         |   4     |
    MICAH                         |   7     |
    NAHUM                         |   3     |
    HABAKKUK                      |   3     |
    ZEPHANIAH                     |   3     |
    HAGGAI                        |   2     |
    ZECHARIAH                     |   14    |
    MALACHI                       |   4     |


## I pray God helps you to see, hear, read and understand and most importantly do something right about it! God bless you on your journey! Thank you for reading.


### [The Visual Bible - The Gospel Of Matthew](https://www.youtube.com/watch?v=woAhReBytBk) [MOVIE]
### [The Gospel of Luke](https://www.youtube.com/watch?v=auL-ebjH-xo) [MOVIE]
### [The Gospel of Luke - Film - Visual Bible in HD Very Rare Version](https://www.youtube.com/watch?v=2PHPLApTt7Y) [MOVIE]
### [The Acts of the Apostles - Film - High Quality! HD](https://www.youtube.com/watch?v=tRXNp6K5-JI) [MOVIE]
### [Paul the Apostle Full Movie](https://www.youtube.com/watch?v=t5FhLQhDsk0) [MOVIE]
### [The Book Of Revelation (Full Movie)](https://www.youtube.com/watch?v=NAb2hdQneBY) [MOVIE]
### [The Ruth Story](https://www.youtube.com/watch?v=slEmSyJi81g) [MOVIE]
### [Esther and the King](https://www.youtube.com/watch?v=SQ6qYypfmIo) [MOVIE]
### [Samson and Delilah - full movie - full movie](https://www.youtube.com/watch?v=a9968bcrywY) [MOVIE]
### [David and Goliath...Orson Welles as King Saul](https://www.youtube.com/watch?v=GpVf6JII-VM) [MOVIE]
### [Sodom & Gomorrah FULL VIDEO](https://www.youtube.com/watch?v=WWpknxvxLpk) [MOVIE]
### [The Story of Joseph and His Brethren (1962)](https://www.youtube.com/watch?v=u2dM_kW-SOI) [MOVIE]
### [Abraham, Sarah, Isaac, Jacob ( Full Movie )](https://www.youtube.com/watch?v=V5WNbtj3gZs) [MOVIE]
### [The Ten Commandments.Full Movie HD.](https://www.youtube.com/watch?v=4s320VeVUQA) [MOVIE]
### [Jesus Of Nazareth (Original Bible Movie) 1977](https://www.youtube.com/watch?v=pG6Y88iQhCE) [MOVIE]
### [Jesus is Coming Full Movie](https://www.youtube.com/watch?v=Gi0eW2BEOXM) [MOVIE]


**Note:** These are old movies, you can trust these more than the new ones having new actors and brainwashing tactics.


### [Paganism Surviving In Christianity](https://www.forgottenbooks.com/en/readbook/PaganismSurvivinginChristianity_10066362) [BOOK]
### [How We Got Our Bible](https://www.forgottenbooks.com/en/readbook/HowWeGotOurBible_10038867) [BOOK]
### [The Negro In Our History](https://www.forgottenbooks.com/en/readbook/TheNegroinOurHistory_10101622) [BOOK]


## THE EARTH IS FLAT, IN CASE YOU DIDN'T KNOW, NASA LIES!

**ISAIAH 40:22:** It is he that sitteth upon the circle of the earth, and the inhabitants thereof are as grasshoppers; that stretcheth out the heavens as a curtain, and spreadeth them out as a tent to dwell in:

**ISAIAH 40:23:** That bringeth the princes to nothing; he maketh the judges of the earth as vanity.

**ISAIAH 40:24:** Yea, they shall not be planted; yea, they shall not be sown: yea, their stock shall not take root in the earth: and he shall also blow upon them, and they shall wither, and the whirlwind shall take them away as stubble.


# THERE IS NO GRAVITY! WAKE UP NEO!

![ImpulsiveNeo](ImpulsiveNeo.jpg)

# THE EARTH IS FLAT! [RESEARCH IT ON YOUTUBE](https://www.youtube.com/results?search_query=flat+earth&page=&utm_source=opensearch)!

# THIS IS POSITIVE INFO! IT'S A MATTER OF PERSPECTIVE!

# THE WAR ON TERROR IS A WAR ON YOU!

## RETARDS - Round Earth Taught Analed Retention Disorder Syndrome

- 0:  [The Greatest Truth Never Told](https://www.youtube.com/watch?v=ekkXHnSrlwY&list=PLD31E34390C5017E8)

- 1:  [Under The Dome - Full Documentary](https://www.youtube.com/watch?v=fk4YqPtvJao)
- 2:  [A History Of Flat Earth - Eric Dubay](https://www.youtube.com/watch?v=pGl8I3l-5ac)
- 3:  [A Flat Earth Awakening Story - Eric Dubay](https://www.youtube.com/watch?v=ER9Ul_ostZ8)
- 4:  [Flat Earth, Fake Aliens and Real Giants](https://www.youtube.com/watch?v=oqPLShx0Jfc)
- 5:  [Giant Human Beings Existed](https://www.youtube.com/watch?v=mRqjY5kyu34)
- 6:  [OUR FLAT DOMED CLOSED SYSTEM EXPLAINED - DMurphy25](https://www.youtube.com/watch?v=-RIBO7VB0VE)
- 7:  [Firmament Rising - The Globular Deception](https://www.youtube.com/watch?v=rez2CmyyfN4)
- 8:  [The Best Flat Earth Documentary](https://www.youtube.com/watch?v=GhRiLP32qfs)
- 9:  [IMPOSSIBALL Flat Earth Documentary (2017)](https://www.youtube.com/watch?v=UbYtkrTquXE)
- 10: [THE BEST Flat Earth VIDEO | 1000% Proof The Earth Is Flat | Lets See You Debunk This!!!!](https://www.youtube.com/watch?v=p7lDq4dOlIk)
- 11: [THE BEST Flat Earth VIDEO FOR All PEOPLE | 100% PROOF THE EARTH IS FLAT](https://www.youtube.com/watch?v=ynnFwTiQlxM)
- 12: [FLAT EARTH - 'Absolute Proof' | Rocket Hitting The Dome](https://www.youtube.com/watch?v=echpThvHli8)
- 13: [200 Proofs Earth is Not a Spinning Ball Videobook](https://www.youtube.com/watch?v=h5i_iDyUTCg)
- 14: [The Zionists, Freemasons, and NASA's Biggest Secret](https://www.youtube.com/watch?v=dTqmcvdm4hM)
- 15: [There are no forests on Flat Earth Wake Up](https://www.youtube.com/watch?v=UHkiZNT3cyE)
- 16: [There are no forests on earth! (ENGLISH VOICEOVER)](https://www.youtube.com/watch?v=ObJL6aA2czo)
- 17: [The World's Biggest Secret](https://www.youtube.com/watch?v=TFsuOFoolW8)
- 18: [Big Bang Evolution is a Masonic Lie Hiding Intelligent Design](https://www.youtube.com/watch?v=JkEL4yBJxm8)
- 19: [Under The Dome - Documentary (Edge of the firmament)](https://www.youtube.com/watch?v=4BxHP9T6480)
- 20: [The Flat Earth History and WHY it's hidden from us. By Eric Dubay. As Talked About with Eddie Bravo!](https://www.youtube.com/watch?v=9UbV3kTY8jw)
- 21: [NASA ISS HOAX! INTERNATIONAL SPACE STATION DOES NOT EXIST!](https://www.youtube.com/watch?v=TSQjerWbRfo)
- 22: [Flat Earth PROOF of God [6/9/2017]](https://www.youtube.com/watch?v=YI3BrH5t7oQ)
- 23: [Flat Earth Dome Explained 100% & the Entrance to Agartha](https://www.youtube.com/watch?v=fDBRhxryfZM)
- 24: [No One Has Been To Space~Watch This!](https://www.youtube.com/watch?v=WHMzgKB_uhY)
- 25: [Flat Earth Evidence and Proof June 2017](https://www.youtube.com/watch?v=-utWNUnrT9g)
- 26: [BEST FLAT EARTH PROOF 2017 - YOU CANT DENY THIS EVIDENCE](https://www.youtube.com/watch?v=awl8Eel7fgg)
- 27: [How to Quit Your Slave Job (and Live Your Dream Life!)](https://www.youtube.com/watch?v=HLwNG5l0Yoo)
- 28: [The Most Important Thing in Your Life](https://www.youtube.com/watch?v=sKH-NmLFDH4)
- 29: [Satan's Computer; What you Where Not Taught In School, This Will Blow Your Mind - Flat Earth Stream](https://www.youtube.com/watch?v=jwK6aUfTrvQ)
- 30: [ANONYMOUS. URGENT MESSAGE: SOCIAL MEDIA AND THE MARK OF THE BEAST. NWO AGENDA ARRIVES](https://www.youtube.com/watch?v=X6plO9aABeQ)
- 31: [The MARK of The BEAST Identified](https://www.youtube.com/watch?v=13RzjyhKz3M)
- 32: [Trump Declares "One World Currency" Sooner than most think (bloomberg)](https://www.youtube.com/watch?v=PuH_wCwxBhw)
- 33: [Devils tower and Pagan rituals](https://www.youtube.com/watch?v=y2dBpiS_Aik)
- 34: [Donald Trump's Saudi Arabia Visit "Orb Ritual" - Melania & Ivanka Are Men!](https://www.youtube.com/watch?v=ktFzCnMn6_Y)
- 35: [Trump will usher in the 7 Noahide Laws ONE WORLD RELIGION](https://www.youtube.com/watch?v=sPEQO-3UqkM)
- 36: [ARCODEAUS - The Noahide Laws - May 20, 2017](https://www.youtube.com/watch?v=oETRa_ExfXA)
- 37: [CHRISTIANS MUST WATCH we are being LIED TO ISRAELITES](https://www.youtube.com/watch?v=xNTdajfE14Y)
- 38: [The TRUE Hebrew Israelites defined by Scripture and history. WARNING you will be shocked!!!](https://www.youtube.com/watch?v=bEDfrBBPZzg)
- 39: [A History of the True Hebrews (Documentary)](https://www.youtube.com/watch?v=biPDp8pGqGg)
- 40: [WHO ARE THE REAL BIBLICAL ISRAELITES?](https://www.youtube.com/watch?v=HuUAnpIPK5E)
- 41: [EUROPEAN CONFESSIONS-AFRICAN AMERICANS ARE THE TRUE ISRAELITES AND THE CHOSEN PEOPLE OF GOD](https://www.youtube.com/watch?v=ja93FjyCSfo)
- 42: [Demonic Sigils and Eyes in the Skies](https://www.youtube.com/watch?v=N-kdx5IhIoc)
- 43: [TELEVISION Will Kill you. PATENT to PROVE it..](https://www.youtube.com/watch?v=15GtRc7ViBk)
- 44: [You Won't Believe What They Admitted on the News in 1971...](https://www.youtube.com/watch?v=yfaAtdTgBGk)
- 45: [Mass Hypnosis and Trigger Words](https://www.youtube.com/watch?v=fznpRaM1wIg)
- 46: [Society Is Being Programmed By A Black Box](https://www.youtube.com/watch?v=rQmIPK7DQh8)
- 47: [The Privacyless, Freedomless Smart City of 2030 the Elite Are Engineering](https://www.youtube.com/watch?v=GRybM76qx6I)
- 48: [Obsolete — Full Documentary Official (2016)](https://www.youtube.com/watch?v=jPmUGq25KBk)
- 49: [Rosa Koire : Smart Cities are Future Agenda 21 Hi-Tech Monitored Concentration](https://www.youtube.com/watch?v=p3XuSo03N7s)
- 50: [Why Are We Literally Eating Demon-Shaped Dead Food in This Society?](https://www.youtube.com/watch?v=EeK_iampjjg)
- 51: [We Are Being Groomed for the Next Big War](https://www.youtube.com/watch?v=poQPBppFyWM)
- 52: [Elon Musk: 'We Must Hack Our Brains or Be Destroyed by AI'](https://www.youtube.com/watch?v=MOs-ib5STPE)
- 53: [NASA's Future of War 2025 Is Already Here! (HD)](https://www.youtube.com/watch?v=aDpGB9J27_g)
- 54: [What Bilderberg Really Wants In 2017](https://www.youtube.com/watch?v=EbFMnrPbAmU)
- 55: [AGENDA 21 THE MOVIE: THE MEGACITIES ARE COMING.](https://www.youtube.com/watch?v=mZhI9vvZ2Wo)
- 56: [This Creepy Patent Proves They Can Remotely Hijack Your Nervous System](https://www.youtube.com/watch?v=yf_EdKxfDiY)
- 57: [Trump's New World Order](https://www.youtube.com/watch?v=eLS5h1ZDKvE)
- 58: [Agenda 21 Smart Cities: Orwell's Dystopic Nightmare Comes True](https://www.youtube.com/watch?v=T9DK0JThOio)
- 59: [Bill Gates Just Warned a New Bioweapon Will Wipe Out 30 Million](https://www.youtube.com/watch?v=sErgwyD2KR0)
- 60: [WOLVES IN SHEEP'S CLOTHING: How the public was duped into socialism, but got totalitarianism](https://www.youtube.com/watch?v=cYgyDjl2nCU)
- 61: [Psywar - Full Documentary](https://www.youtube.com/watch?v=2eB046f998U)
- 62: [We Are Becoming the Internet, the Internet Is Becoming Us](https://www.youtube.com/watch?v=GnLyjsO7mZc)
- 63: [The Real Secrets Hidden in Antarctica... Revealed](https://www.youtube.com/watch?v=237F1_aLXZ8)
- 64: [6 Secret Cities That Prove We Don't Know What's Really Going On](https://www.youtube.com/watch?v=wYyBcOLq8bs)
- 65: [Two Top Secret Missions Disguised As Historic Moments You Thought Were Real](https://www.youtube.com/watch?v=1ZiQUngMhr4)
- 66: [AGENDA 21 THE MOVIE: THE MEGACITIES ARE COMING.](https://www.youtube.com/watch?v=mZhI9vvZ2Wo)
- 67: [POWERUL TESTIMONY!! THIS MAN SAW HITLER AND OTHER EVIL PEOPLE IN HELL DURING A NEAR DEATH EXPERIENCE](https://www.youtube.com/watch?v=xt9xodhZ5KI)
- 68: [Aaliyah, Lefteye,Biggie,Eazy E,Whitney Houston, Amy Winehouse Are All N Hell](https://www.youtube.com/watch?v=wwUffrMRDqE)
- 69: [CELEBRITIES SEEN IN HELL (TUPAC, ROBIN WILLIAMS, ELVIS, HEATH LEDGER, AND MORE)](https://www.youtube.com/watch?v=_gNw4SGGwDU)
- 70: [INDIA IMPLEMENTING THE BEAST SYSTEM. CAN'T BUY OR SELL UNLESS YOU TAKE A 12 DIGIT NUMBER](https://www.youtube.com/watch?v=ppEDMsnMfJw)
- 71: [HITLER: Negroes are The True Jews](https://www.youtube.com/watch?v=NE-X985_prM)
- 72: [Blacks are in fact the true jews of the bible](https://www.youtube.com/watch?v=FaqCyBlwCxQ&list=PLA3OCbJL135SGuahCKhuQ20eKMiSdXm2t)
- 73: [THE TRUTH ON THE REAL HEBREW ISRAELITES IS OUT AND THE NATIONS ARE TERRIFIED !!!!!!](https://www.youtube.com/watch?v=mP2ivfkfHVM)
- 74: [Video 10- Testimonies of Edomites/Gentiles Telling Blacks They Are the True Hebrew Israelites](https://www.youtube.com/watch?v=qhjajMbTX1Y)
- 75: [Pt 1 Even the Syrian Refugees Know the Real Hebrew Israelites are Black](https://www.youtube.com/watch?v=YWjd36NOGBg)
- 76: [The Real Hebrews](https://www.youtube.com/watch?v=WvqvteApUGQ)
- 77: [The Real Hebrews 2](https://www.youtube.com/watch?v=IgGXD5nqWXQ&spfreload=1)
- 78: [Adolf Hitler The greatest story Never told Full 6 hours Documentary](https://www.youtube.com/watch?v=7XExjrZxTdk)
- 79: [World Defeated The Wrong Enemy](https://www.youtube.com/watch?v=bm34sj65MkA)
- 80: [Become a Holocaust Denier in 14 Minutes](https://www.youtube.com/watch?v=XEZkvsK7nfo)
- 81: [David Irving Exposes The Holocaust Legend](https://www.youtube.com/watch?v=mYCwaIt-GUM)
- 82: [Celebrities speaking about Zionist Jews](https://www.youtube.com/watch?v=_xchaB_JcAY)
- 83: [EVERYONE NEEDS TO WATCH THIS!! The Protocols of Zion Full Movie](https://www.youtube.com/watch?v=sWjWGVYCMvg)
- 84: [David Irving - Jailed and Beaten For Telling Truth of 2nd World War](https://www.youtube.com/watch?v=8cAFpi4tHMM)
- 85: [The Deleted Interview that George Soros Tried to Ban!](https://www.youtube.com/watch?v=SUdosc33eSE)
- 86: [The Illustrated Protocols of Zion by David Duke](https://www.youtube.com/watch?v=d-xjLa9xrOo)
- 87: [Protocols of Zion The Roadway to destroy America (RichieFromBoston)](https://www.youtube.com/watch?v=848o93RAJtA)
- 88: [Why the Jewish Elite Hates Donald Trump](https://www.youtube.com/watch?v=HV2GhOkQ1yY)
- 89: [Do Zionists Control Wall Street? The Shocking Facts!](https://www.youtube.com/watch?v=pUY7o7pX6vk)
- 90: [Ahmadinejad: They're finished, the Zionist regime is finished.](https://www.youtube.com/watch?v=oLkiM4CHAJo)
- 91: [Israelis Are Not Jews and American Leaders Are Not Christian](https://www.youtube.com/watch?v=PrWguVsEih0)
- 92: [Ahmadinejad on Jews - Larry King](https://www.youtube.com/watch?v=_vYXcna8Pxw)
- 93: [Charlie Rose - Dr. Mahmoud Ahmadinejad, President of Islamic Republic of Iran | Sept. 20, 2010](https://www.youtube.com/watch?v=Im_bRb8CKDk)
- 94: [Mein Kampf - Audio Book](https://www.youtube.com/watch?v=xDOPHZC936c)
- 95: [08/08/2006 President Ahmadinejad Interview](https://www.youtube.com/watch?v=bFCUX5JSA14)
- 96: [Assad say’s “Trumps a Puppet” to Indian media مقابلة الرئيس الأسد مع قناة ويون الهندية](https://www.youtube.com/watch?v=SxpvoVGXURM)
- 97: [Assad smashes journalist with facts in Interview, Oct 6 (مقابلة الرئيس الأسد مع قناة TV2 الدانماركية](https://www.youtube.com/watch?v=7ItP5bLZ8H8)
- 98: [Manchester Bombing False Flag, Pushing the War on Terror (CorbettReport Mirror)](https://www.youtube.com/watch?v=zObCqOaWjh4)
- 99: [False Flag Operations - 9/11, Sandy Hook, Boston Bombing and more - 2016](https://www.youtube.com/watch?v=CQN6wXfQvok)
- 100:[False Flag Alien Event - Don't Fall For It When It Happens!](https://www.youtube.com/watch?v=HF2cBYDvVS8)
- 101:[CAUGHT!!!- State Trucks Poisoning Neighborhoods](https://www.youtube.com/watch?v=bz0-w6zDIT0)
- 102:[City spraying more due to surge in mosquitoes](https://www.youtube.com/watch?v=cOuOqZioiHk)
- 103:[Syria’s Assad BRILLIANTLY Explained How America REALLY Works](https://www.youtube.com/watch?v=zrXvhy8Y57M)
- 104:[Benghazi Whistleblowers – The story behind the cover-up - CTM #670](https://www.youtube.com/watch?v=_vUJSvynuxw)
- 105:[March 22, 2017 U.K. Parliament "terrorism" attack is false flag propaganda / hoax](https://www.youtube.com/watch?v=v3tL_wF-COg)
- 106:[Paris Attack False Flag: Conspiracy Hoax Exposed](https://www.youtube.com/watch?v=OXavIbOQnZw)
- 107:[HOAX GERMAN FALSE FLAG ATTACK.."Return of the Crisis actor III" Lites film action!](https://www.youtube.com/watch?v=-0AeRIjfO0M)
- 108:[Berlin Christmas Market Truck Massacre Hoax](https://www.youtube.com/watch?v=A3aoIenOgdM)
- 109:[Nice France Terror Attack Staged 100% FAKE](https://www.youtube.com/watch?v=SrbNtFfMQ4A)
- 110:[7 CONFIRMED False Flag Attacks](https://www.youtube.com/watch?v=Gst2pwtzz1w)
- 111:[Steve Hughes on war on terror, global warming and X-factor.](https://www.youtube.com/watch?v=Nea-MpVgRL0&list=RDhMcS82DpjSU)
- 112:[Jim Jeffries on America's "freedom"](https://www.youtube.com/watch?v=bjeq3NYUw2M)
- 113:[Donald Trump False Flag Assassination](https://www.youtube.com/watch?v=f9zUeCztKCA)
- 114:[The Untold Story of Adolf Hitler - RFG Chosen 1 & Bro. Sanchez](https://www.youtube.com/watch?v=Q7HhLS7584g)
- 115:[Hillary Clinton & Donald Trump are Cousins EXPOSED!](https://www.youtube.com/watch?v=LuEaf_6P7QY)
- 116:[Biggest False Flag Operation Since 9 11 Happening Right Now!](https://www.youtube.com/watch?v=r_aozYvb_Rs)
- 117:[THIS IS HAPPENING RIGHT BEFORE OUR EYES AND NO ONE SEE'S THE BIGGER ](https://www.youtube.com/watch?v=KjkDqzhCq0c)
- 118:[WHAT DO BANKS, RAILROADS, RETAIL STORES, STANDARD OIL, LUMBER & THE FOOD ](https://www.youtube.com/watch?v=ZI1YUe2oYEQ)
- 119:[A PICTURE IS WORTH A THOUSAND WORDS!](https://www.youtube.com/watch?v=HFTcjSHzyxM)
- 120:[Playing the Trump Card: Obama’s 3rd Term and WW3 (Trump's false flag assassination](https://www.youtube.com/watch?v=HuF14oF2D2Q)
- 121:[IS A 3RD TERM FOR BARACK OBAMA STILL POSSIBLE??? (RIGGED ELECTIONS 2016)](https://www.youtube.com/watch?v=Ol44a2xChqM)
- 122:[This is why Scalia was Murdered](https://www.youtube.com/watch?v=wyPFbDP8W6I)
- 123:[SGTreport: The Paris False Flag of "TRUTH" -- Dr. Paul Craig Roberts](https://www.youtube.com/watch?v=6kSugZtgXsc)
- 124:[Donald Trump - Illuminati Puppet Exposed - Part 1](https://www.youtube.com/watch?v=SL_uAY63IWo)
- 125:[Donald Trump - Illuminati Puppet Exposed - Part 2](https://www.youtube.com/watch?v=7vRHwTZCt7Q&list=RD7vRHwTZCt7Q#t=29)
- 126:[Donald Trump - Controlled by the Illuminati? New World Order MUST WATCH](https://www.youtube.com/watch?v=TXpOiB2kdIM)
- 127:[GISELE TOM BRADY ILLUMINATI TRANNY COUPLE EXPOSED!](https://www.youtube.com/watch?v=FMG4GUgnlMo)
- 128:[MEGYN KELLY ILLUMINATI TRANNY EXPOSED!](https://www.youtube.com/watch?v=t5j1CPUf9RI)
- 129:[2 Different Melania Trump Actresses IMO. Side By Side Split Screen.](https://www.youtube.com/watch?v=zsD7e8NUZO8)

### [Lesson in Psychology](https://www.youtube.com/watch?v=vo4pMVb0R6M&list=PL8dPuuaLjXtOPRKzVLY0jJY-uHOH9KVU6)

**Note:** If some of the youtube video links above don't work, search for the video by name in the youtube search

## God is so kind that it is impossible to imagine His unbounded kindness

![flat-earth-isaiah40-22](flat-earth-isaiah40-22.jpg)

# WHAT DOES THE REAL WORLD LOOK LIKE?

![Flat Earth; Exposing the Jesuit Agenda! 4](Flat-Earth-Exposing-the-Jesuit-Agenda-4.png)

# PRAISE GOD FOR THE FLAT EARTH TRUTH! JESUS LIVES!

![Gleasons-New-Standard-Map](Gleasons-New-Standard-Map.jpg)

![flat-earth-model](flat-earth-model.gif)

![SunAnimation](SunAnimation.gif)

# BE KIND TO EACH OTHER

![56f6b029eb00d9b24cc7470fd0a68468](56f6b029eb00d9b24cc7470fd0a68468.jpg)

# WAKE UP! KNOCK KNOCK WAKE UP!

![Globe](globe_1.jpg)

![zion-pyramid](zion-pyramid.png)

# AUDIOBIBLE HEAR PSALMS 71

## OPEN YOUR MIND! BREAK FREE FROM THE LIES AND SATANIC PROGRAMMING!

[![jwish-parliamnetbannedweb-sizeweb](jwish-parliamnetbannedweb-sizeweb.jpg)](https://www.youtube.com/user/drdduke)

# HISTORY REPEATS ITSELF

![holocaust-is-a-hoax](holocaust-is-a-hoax.png)

![hitler-facts](hitler-facts.png)

# THE WAR ON THE PEOPLE NEVER ENDED

![jews-declare-war-on-germany](jews-declare-war-on-germany.png)

![germany1](germany1.png)

![germany2](germany2.png)

![american-genocide](american-genocide.png)

![last-indian-massacre](last-indian-massacre.png)

![red-indians-wiped-out-and-re-educated](red-indians-wiped-out-and-re-educated.png)

![usa-mexican-repatriation-act1](usa-mexican-repatriation-act1.png)

![usa-mexican-repatriation-act2](usa-mexican-repatriation-act2.png)

![jesse-owens-story](jesse-owens-story.png)

![german-troops](german-troops.png)

![western-powers-are-liars](western-powers-are-liars.png)

![he-didnt-want-war-he-only-wanted-peace](he-didnt-want-war-he-only-wanted-peace.png)

![roosevelt-churchill](roosevelt-churchill.png)

![roosevelt-churchill-stalin-war-criminals](roosevelt-churchill-stalin-war-criminals.png)

![false-witness-rudolf-hoss](false-witness-rudolf-hoss.png)

![german-atrocities-misleading](german-atrocities-misleading.png)

![no-proof-hitler-ordered-killing-of-jews](no-proof-hitler-ordered-killing-of-jews.png)

![no-witnesses-no-pohotos-nothing-of-gassed-victims](no-witnesses-no-pohotos-nothing-of-gassed-victims.png)

![hitler-on-zionists](hitler-on-zionists.png)

![protocol-of-zion1](protocol-of-zion1.png)

![protocol-of-zion2](protocol-of-zion2.png)

![protocol-of-zion3](protocol-of-zion3.png)

![protocol-of-zion4](protocol-of-zion4.png)

![protocol-of-zion5](protocol-of-zion5.png)

![protocol-of-zion6](protocol-of-zion6.png)

![henry-ford-on-protocols-of-zion](henry-ford-on-protocols-of-zion.png)

![manufactured-terrorism](manufactured-terrorism.png)

# THEY ARE THE SAME ONES WHO CRUCIFIED JESUS

![INRI](INRI.png)

# AUDIOBIBLE FIND CROWN OF LIFE

## HERE IS A FLIER YOU CAN PRINT AND GIVE OUT TO PEOPLE

![youtube-search-flat-earth-letter](youtube-search-flat-earth-letter.jpg)

## WARNING! DEMONIC SIGILS OF SUMMONING! FOR EDUCATIONAL PURPOSES!

![Demons](demons.png)