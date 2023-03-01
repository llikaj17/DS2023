# coding=utf-8
# Reference: AngryBERT processing pipeline
"""
# CLeaning Pipeline Reference
@inproceedings{angrybert21,
    title={AngryBERT: Joint Learning Target and Emotion for Hate Speech Detection},
    author={Awal, Md Rabiul and Cao, Rui and Lee, Roy Ka-Wei and Mitrovi{\'{c}}, Sandra},
    booktitle={25th Pacific-Asia Conference on Knowledge Discovery and Data Mining},
    year={2021},
    organization={Springer}
}
from https://gitlab.com/bottle_shop/safe/angrybert/-/tree/master/
"""

import json
import re
import string

import wordninja
import splitter
from nltk.tokenize.treebank import TreebankWordTokenizer
import numpy as np

# Aphost lookup dict
symbols_to_delete = '@＼・ω+=”“[]^>\\°<~•≠™ˈʊɒ∞§{}·τα❤☺ɡ|¢→̶`❥━┣┫┗Ｏ►★©―ɪ✔®\x96\x92●£♥➤´¹☕≈÷♡◐║▬′ɔː€۩۞†μ✒➥═☆ˌ◄½ʻπδηλσερνʃ✬ＳＵＰＥＲＩＴ☻±♍µº¾✓◾؟．⬅℅»Вав❣⋅¿¬♫ＣＭβ█▓▒░⇒⭐›¡₂₃❧▰▔◞▀▂▃▄▅▆▇↙γ̄″☹➡«φ⅓„✋：¥̲̅́∙‛◇✏▷❓❗¶˚˙）сиʿ✨。ɑ\x80◕！％¯−ﬂﬁ₁²ʌ¼⁴⁄₄⌠♭✘╪▶☭✭♪☔☠♂☃☎✈✌✰❆☙○‣⚓年∎ℒ▪▙☏⅛ｃａｓǀ℮¸ｗ‚∼‖ℳ❄←☼⋆ʒ⊂、⅔¨͡๏⚾⚽Φ×θ￦？（℃⏩☮⚠月✊❌⭕▸■⇌☐☑⚡☄ǫ╭∩╮，例＞ʕɐ̣Δ₀✞┈╱╲▏▕┃╰▊▋╯┳┊≥☒↑☝ɹ✅☛♩☞ＡＪＢ◔◡↓♀⬆̱ℏ\x91⠀ˤ╚↺⇤∏✾◦♬³の｜／∵∴√Ω¤☜▲↳▫‿⬇✧ｏｖｍ－２０８＇‰≤∕ˆ⚜☁.,?!;*"…:—()%$&/\n🍕\r🐵😑\xa0\ue014\t\uf818\uf04a\xad😢🐶️\uf0e0😜😎👊\u200b\u200e😁عدويهصقأناخلىبمغر😍💖💵Е👎😀😂\u202a\u202c🔥😄🏻💥ᴍʏʀᴇɴᴅᴏᴀᴋʜᴜʟᴛᴄᴘʙғᴊᴡɢ😋👏שלוםבי😱‼\x81エンジ故障\u2009🚌ᴵ͞🌟😊😳😧🙀😐😕\u200f👍😮😃😘אעכח💩💯⛽🚄🏼ஜ😖ᴠ🚲‐😟😈💪🙏🎯🌹😇💔😡\x7f👌ἐὶήιὲκἀίῃἴξ🙄Ｈ😠\ufeff\u2028😉😤⛺🙂\u3000تحكسة👮💙فزط😏🍾🎉😞\u2008🏾😅😭👻😥😔😓🏽🎆🍻🍽🎶🌺🤔😪\x08‑🐰🐇🐱🙆😨🙃💕𝘊𝘦𝘳𝘢𝘵𝘰𝘤𝘺𝘴𝘪𝘧𝘮𝘣💗💚地獄谷улкнПоАН🐾🐕😆ה🔗🚽歌舞伎🙈😴🏿🤗🇺🇸мυтѕ⤵🏆🎃😩\u200a🌠🐟💫💰💎эпрд\x95🖐🙅⛲🍰🤐👆🙌\u2002💛🙁👀🙊🙉\u2004ˢᵒʳʸᴼᴷᴺʷᵗʰᵉᵘ\x13🚬🤓\ue602😵άοόςέὸתמדףנרךצט😒͝🆕👅👥👄🔄🔤👉👤👶👲🔛🎓\uf0b7\uf04c\x9f\x10成都😣⏺😌🤑🌏😯ех😲Ἰᾶὁ💞🚓🔔📚🏀👐\u202d💤🍇\ue613小土豆🏡❔⁉\u202f👠》कर्मा🇹🇼🌸蔡英文🌞🎲レクサス😛外国人关系Сб💋💀🎄💜🤢َِьыгя不是\x9c\x9d🗑\u2005💃📣👿༼つ༽😰ḷЗз▱ц￼🤣卖温哥华议会下降你失去所有的钱加拿大坏税骗子🐝ツ🎅\x85🍺آإشء🎵🌎͟ἔ油别克🤡🤥😬🤧й\u2003🚀🤴ʲшчИОРФДЯМюж😝🖑ὐύύ特殊作戦群щ💨圆明园קℐ🏈😺🌍⏏ệ🍔🐮🍁🍆🍑🌮🌯🤦\u200d𝓒𝓲𝓿𝓵안영하세요ЖљКћ🍀😫🤤ῦ我出生在了可以说普通话汉语好极🎼🕺🍸🥂🗽🎇🎊🆘🤠👩🖒🚪天一家⚲\u2006⚭⚆⬭⬯⏖新✀╌🇫🇷🇩🇪🇮🇬🇧😷🇨🇦ХШ🌐\x1f杀鸡给猴看ʁ𝗪𝗵𝗲𝗻𝘆𝗼𝘂𝗿𝗮𝗹𝗶𝘇𝗯𝘁𝗰𝘀𝘅𝗽𝘄𝗱📺ϖ\u2000үսᴦᎥһͺ\u2007հ\u2001ɩｙｅ൦ｌƽｈ𝐓𝐡𝐞𝐫𝐮𝐝𝐚𝐃𝐜𝐩𝐭𝐢𝐨𝐧Ƅᴨןᑯ໐ΤᏧ௦Іᴑ܁𝐬𝐰𝐲𝐛𝐦𝐯𝐑𝐙𝐣𝐇𝐂𝐘𝟎ԜТᗞ౦〔Ꭻ𝐳𝐔𝐱𝟔𝟓𝐅🐋ﬃ💘💓ё𝘥𝘯𝘶💐🌋🌄🌅𝙬𝙖𝙨𝙤𝙣𝙡𝙮𝙘𝙠𝙚𝙙𝙜𝙧𝙥𝙩𝙪𝙗𝙞𝙝𝙛👺🐷ℋ𝐀𝐥𝐪🚶𝙢Ἱ🤘ͦ💸ج패티Ｗ𝙇ᵻ👂👃ɜ🎫\uf0a7БУі🚢🚂ગુજરાતીῆ🏃𝓬𝓻𝓴𝓮𝓽𝓼☘﴾̯﴿₽\ue807𝑻𝒆𝒍𝒕𝒉𝒓𝒖𝒂𝒏𝒅𝒔𝒎𝒗𝒊👽😙\u200cЛ‒🎾👹⎌🏒⛸公寓养宠物吗🏄🐀🚑🤷操美𝒑𝒚𝒐𝑴🤙🐒欢迎来到阿拉斯ספ𝙫🐈𝒌𝙊𝙭𝙆𝙋𝙍𝘼𝙅ﷻ🦄巨收赢得白鬼愤怒要买额ẽ🚗🐳𝟏𝐟𝟖𝟑𝟕𝒄𝟗𝐠𝙄𝙃👇锟斤拷𝗢𝟳𝟱𝟬⦁マルハニチロ株式社⛷한국어ㄸㅓ니͜ʖ𝘿𝙔₵𝒩ℯ𝒾𝓁𝒶𝓉𝓇𝓊𝓃𝓈𝓅ℴ𝒻𝒽𝓀𝓌𝒸𝓎𝙏ζ𝙟𝘃𝗺𝟮𝟭𝟯𝟲👋🦊多伦🐽🎻🎹⛓🏹🍷🦆为和中友谊祝贺与其想象对法如直接问用自己猜本传教士没积唯认识基督徒曾经让相信耶稣复活死怪他但当们聊些政治题时候战胜因圣把全堂结婚孩恐惧且栗谓这样还♾🎸🤕🤒⛑🎁批判检讨🏝🦁🙋😶쥐스탱트뤼도석유가격인상이경제황을렵게만들지않록잘관리해야합다캐나에서대마초와화약금의품런성분갈때는반드시허된사용🔫👁凸ὰ💲🗯𝙈Ἄ𝒇𝒈𝒘𝒃𝑬𝑶𝕾𝖙𝖗𝖆𝖎𝖌𝖍𝖕𝖊𝖔𝖑𝖉𝖓𝖐𝖜𝖞𝖚𝖇𝕿𝖘𝖄𝖛𝖒𝖋𝖂𝕴𝖟𝖈𝕸👑🚿💡知彼百\uf005𝙀𝒛𝑲𝑳𝑾𝒋𝟒😦𝙒𝘾𝘽🏐𝘩𝘨ὼṑ𝑱𝑹𝑫𝑵𝑪🇰🇵👾ᓇᒧᔭᐃᐧᐦᑳᐨᓃᓂᑲᐸᑭᑎᓀᐣ🐄🎈🔨🐎🤞🐸💟🎰🌝🛳点击查版🍭𝑥𝑦𝑧ＮＧ👣\uf020っ🏉ф💭🎥Ξ🐴👨🤳🦍\x0b🍩𝑯𝒒😗𝟐🏂👳🍗🕉🐲چی𝑮𝗕𝗴🍒ꜥⲣⲏ🐑⏰鉄リ事件ї💊「」\uf203\uf09a\uf222\ue608\uf202\uf099\uf469\ue607\uf410\ue600燻製シ虚偽屁理屈Г𝑩𝑰𝒀𝑺🌤𝗳𝗜𝗙𝗦𝗧🍊ὺἈἡχῖΛ⤏🇳𝒙ψՁմեռայինրւդձ冬至ὀ𝒁🔹🤚🍎𝑷🐂💅𝘬𝘱𝘸𝘷𝘐𝘭𝘓𝘖𝘹𝘲𝘫کΒώ💢ΜΟΝΑΕ🇱♲𝝈↴💒⊘Ȼ🚴🖕🖤🥘📍👈➕🚫🎨🌑🐻𝐎𝐍𝐊𝑭🤖🎎😼🕷ｇｒｎｔｉｄｕｆｂｋ𝟰🇴🇭🇻🇲𝗞𝗭𝗘𝗤👼📉🍟🍦🌈🔭《🐊🐍\uf10aლڡ🐦\U0001f92f\U0001f92a🐡💳ἱ🙇𝗸𝗟𝗠𝗷🥜さようなら🔼'
tokenizer = TreebankWordTokenizer()
remove_dict = {ord(c): '' for c in symbols_to_delete}


def handle_contractions(x):
    x = tokenizer.tokenize(x)
    # TODO: Implement word split in concatenated words
    return x


def handle_punctuation(x):
    x = x.translate(remove_dict)
    return x


def fix_quote(x):
    x = [x_[1:] if x_.startswith("'") else x_ for x_ in x]
    x = ' '.join(x)
    return x


def preprocess(x):
    x = handle_punctuation(x)
    # x = handle_contractions(x)
    # x = fix_quote(x)
    return x


fill = {"ain't": "is not", "aren't": "are not", "can't": "cannot",
        "can't've": "cannot have", "'cause": "because", "could've": "could have",
        "couldn't": "could not", "couldn't've": "could not have", "didn't": "did not",
        "doesn't": "does not", "don't": "do not", "hadn't": "had not",
        "hadn't've": "had not have", "hasn't": "has not", "haven't": "have not",
        "he'd": "he would", "he'd've": "he would have", "he'll": "he will",
        "he'll've": "he he will have", "he's": "he is", "how'd": "how did",
        "how'd'y": "how do you", "how'll": "how will", "how's": "how is",
        "I'd": "I would", "I'd've": "I would have", "I'll": "I will",
        "I'll've": "I will have", "I'm": "I am", "I've": "I have",
        "i'd": "i would", "i'd've": "i would have", "i'll": "i will",
        "i'll've": "i will have", "i'm": "i am", "i've": "i have",
        "isn't": "is not", "it'd": "it would", "it'd've": "it would have",
        "it'll": "it will", "it'll've": "it will have", "it's": "it is",
        "let's": "let us", "ma'am": "madam", "mayn't": "may not",
        "might've": "might have", "mightn't": "might not", "mightn't've": "might not have",
        "must've": "must have", "mustn't": "must not", "mustn't've": "must not have",
        "needn't": "need not", "needn't've": "need not have", "o'clock": "of the clock",
        "oughtn't": "ought not", "oughtn't've": "ought not have", "shan't": "shall not",
        "sha'n't": "shall not", "shan't've": "shall not have", "she'd": "she would",
        "she'd've": "she would have", "she'll": "she will", "she'll've": "she will have",
        "she's": "she is", "should've": "should have", "shouldn't": "should not",
        "shouldn't've": "should not have", "so've": "so have", "so's": "so as",
        "this's": "this is",
        "that'd": "that would", "that'd've": "that would have", "that's": "that is",
        "there'd": "there would", "there'd've": "there would have", "there's": "there is",
        "they'd": "they would", "they'd've": "they would have", "they'll": "they will",
        "they'll've": "they will have", "they're": "they are", "they've": "they have",
        "to've": "to have", "wasn't": "was not", "we'd": "we would",
        "we'd've": "we would have", "we'll": "we will", "we'll've": "we will have",
        "we're": "we are", "we've": "we have", "weren't": "were not",
        "what'll": "what will", "what'll've": "what will have", "what're": "what are",
        "what's": "what is", "what've": "what have", "when's": "when is",
        "when've": "when have", "where'd": "where did", "where's": "where is",
        "where've": "where have", "who'll": "who will", "who'll've": "who will have",
        "who's": "who is", "who've": "who have", "why's": "why is",
        "why've": "why have", "will've": "will have", "won't": "will not",
        "won't've": "will not have", "would've": "would have", "wouldn't": "would not",
        "wouldn't've": "would not have", "y'all": "you all", "y'all'd": "you all would",
        "y'all'd've": "you all would have", "y'all're": "you all are", "y'all've": "you all have",
        "you'd": "you would", "you'd've": "you would have", "you'll": "you will",
        "you'll've": "you will have", "you're": "you are", "you've": "you have", "u.s.": "united states",
        "#lol": "laughing out loud", "#lamo": "laughing my ass off", "#rof": "rolling on the floor laughing",
        "#covfefe": "ironic", "wtf": "what the fuck", "#wtf": "what the fuck",
        "tbh": "to be honest"}

slang = {
    "4ward": "forward",
    "brb": "be right back",
    "b4": "before",
    "bfn": "bye for now",
    "bgd": "background",
    "btw": "by the way",
    "br": "best regards",
    "clk": "click",
    "da": "the",
    "deet": "detail",
    "deets": "details",
    "dm": "direct message",
    "f2f": "face to face",
    "ftl": " for the loss",
    "ftw": "for the win",
    "f**k": "fuck",
    "f**ked": "fucked",
    "b***ch": "bitch",
    "kk": "cool cool",
    "kewl": "cool",
    "smh": "so much hate",
    "yaass": "yes",
    "a$$": "ass",
    "bby": "baby",
    "bc": "because",
    "coz": "because",
    "cuz": "because",
    "cause": "because",
    "cmon": "come on",
    "cmonn": "come on",
    "dafuq": "what the fuck",
    "dafuk": "what the fuck",
    "dis": "this",
    "diss": "this",
    "ma": "my",
    "dono": "do not know",
    "donno": "do not know",
    "dunno": "do not know",
    "fb": "facebook",
    "couldnt": "could not",
    "n": "and",
    "gtg": "got to go",
    "yep": "yes",
    "yw": "you are welcome",
    "im": "i am",
    "youre": "you are",
    "hes": "he is",
    "shes": "she is",
    "theyre": "they are",
    "af": "as fuck",
    "em": "them",
    "rip": "rest in peace",
    "mfs": "mother fuckers",
    "69": "sixty nine",
    "fam": "family",
    "fwd": "forward",
    "ffs": "for fuck sake",
    "fml": "fuck my life",
    "lol": "laugh out loud",
    "lel": "laugh out loud",
    "lool": "laugh out loud",
    "lmao": "laugh my ass off",
    "lmaoo": "laugh my ass off",
    "omg": "oh my god",
    "oomg": "oh my god",
    "omgg": "oh my god",
    "omfg": "oh my fucking god",
    "stfu": "shut the fuck up",
    "awsome": "awesome",
    "imo": "in my opinion",
    "imho": "in my humble opinion",
    "ily": "i love you",
    "ilyy": "i love you",
    "ikr": "i know right",
    "ikrr": "i know right",
    "idk": "i do not know",
    "jk": "joking",
    "lmk": "let me know",
    "nsfw": "not safe for work",
    "havin": "having",
    "hehe": "haha",
    "tmrw": "tomorrow",
    "yt": "youtube",
    "hahaha": "haha",
    "hihi": "haha",
    "pls": "please",
    "ppl": "people",
    "wtf": "what the fuck",
    "wth": "what teh hell",
    "obv": "obviously",
    "nomore": "no more",
    "u": "you",
    "ur": "your",
    "wanna": "want to",
    "luv": "love",
    "imma": "i am",
    "&": "and",
    "thanx": "thanks",
    "til": "until",
    "till": "until",
    "thx": "thanks",
    "pic": "picture",
    "pics": "pictures",
    "gp": "doctor",
    "xmas": "christmas",
    "rlly": "really",
    "boi": "boy",
    "boii": "boy",
    "rly": "really",
    "whch": "which",
    "awee": "awsome",  # or maybe awesome is better
    "sux": "sucks",
    "nd": "and",
    "fav": "favourite",
    "frnds": "friends",
    "info": "information",
    "loml": "love of my life",
    "bffl": "best friend for life",
    "gg": "goog game",
    "xx": "love",
    "xoxo": "love",
    "thats": "that is",
    "homie": "best friend",
    "homies": "best friends",
    "didn": "did not"
}


def word_splitter(token):
    _splits = splitter.split(token[1:])
    _ninjas = wordninja.split(token[1:])

    word_splits = _splits if len(_ninjas) > len(_splits) else _ninjas

    if len(token) + 1 / 2 < len(word_splits):
        return token

    if word_splits:
        token = ' '.join(word_splits)
    else:
        token = token
    return token


def hashtag_solver(token):
    if token.startswith('#') and token[1:].isupper():
        return token[1:]

    if token.startswith('#'):
        # word_splits = re.sub(r"([A-Z])", r" \1", word[1:]).split()
        myString = re.sub(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))', r' \1', token[1:])
        word_splits = myString.split()
        # print("Splitter {}".format(word_splits))
        if len(word_splits) > 1:
            token = ' '.join(word_splits)
            # print("if {} ### {}".format(tmp, token))
        else:
            token = word_splitter(token)
            # print("Else {} ### {}".format(tmp, token))

    return token


def normalize_word(word):
    temp = word
    while True:
        w = re.sub(r"([a-zA-Z])\1\1", r"\1\1", temp)
        if w == temp:
            break
        else:
            temp = w
    return w


def remove_emoji(string):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)


def refer_normalize(tokens):
    words = []
    for idx in range(len(tokens)):
        if idx + 1 != len(tokens) and tokens[idx].startswith("@") and tokens[idx + 1].startswith("@"):
            continue
        else:
            words.append(tokens[idx])
    return words


def clean_text(text):
    # remove url
    text = re.sub(r'http\S+', '', text)

    # fixing apostrope
    text = text.replace("’", "'")

    # remove &amp;
    text = text.replace('&amp;', 'and ')

    # remove \n
    text = re.sub("\\n", "", text)

    # remove leaky elements like ip,user
    text = re.sub("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", "", text)

    # (')aphostophe  replacement (ie)   you're --> you are
    # ( basic dictionary lookup : master dictionary present in a hidden block of code)
    # tokenizer = TweetTokenizer()
    tokens = text.split()
    tokens = refer_normalize(tokens)
    tokens = [fill[word] if word in fill else word for word in tokens]
    tokens = [fill[word.lower()] if word.lower() in fill else word for word in tokens]
    tokens = [slang[word] if word in slang else word for word in tokens]
    tokens = [slang[word.lower()] if word.lower() in slang else word for word in tokens]
    tokens = [hashtag_solver(word) for word in tokens]
    tokens = [normalize_word(word) for word in tokens]
    exclude = set(string.punctuation)
    text = ' '.join(ch for ch in tokens if ch not in exclude)

    # removing usernames
    text = re.sub("'s", "", text)
    text = re.sub("'", "", text)
    mention_pattern = re.compile(r'@\w*')
    text = re.sub(pattern=mention_pattern, repl='<USER>', string=text)

    # emoji remover
    text = remove_emoji(text)

    text = re.sub("&#\S+", "", text)
    text = re.sub("RT :", "", text)
    # remove non-ascii
    # text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    # text = re.sub(r'[^\w\s]', '', text)

    # to lower
    text = preprocess(text).lower()

    return text


def dump(data):
    def default(obj):
        if type(obj).__module__ == np.__name__:
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            else:
                return obj.item()
        raise TypeError('Unknown type:', type(obj))

    json.dumps(data, default=default)


if __name__ == '__main__':
    txt = "@Jeremy_Hunt @yttr trying to sneak Junior doctors contracts through while media focussed on Chilcott?? You utter cunt. #Fuckyouandyourtoryparty"
    test_1 = clean_text(txt)
    print(test_1)

    txt = "@Jeremy_Hunt @yttr trying to sneak Junior doctors contracts through while media focussed on Chilcott?? You utter cunt. #Fuckyouandyourtoryparty @Jeremy_Hunt lmaoo havin #secondhanded mindfuckability 5th wheeling for the Niners Seahawks SNF game? \n\nFuck it 😬"
    test_2 = clean_text(txt)
    print(test_2)
