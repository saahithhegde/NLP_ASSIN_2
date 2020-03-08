#read the file
def readinput(path):
    f = open(path, "r")
    f = f.read()
    return f

#lets get each word and tag
def preprocess(contents):
    pairs = contents.split()
    for i in range(0, len(pairs)):
        pairs[i] = pairs[i].split('_')
    return pairs


def models(input,flines):
    #calculate all the tag counts
    tag_dic={}
    for line in flines:
        line=preprocess(line)
        for wordtag in line:
            if wordtag[1] not in tag_dic:
                # setting it to one
                tag_dic[wordtag[1]] =1
            else:
                # adding unigram count
                tag_dic[wordtag[1]] += 1
    #print(tag_dic)

    #calculate all the words given tags counts
    words_given_tags={}
    for line in flines:
        line = preprocess(line)
        for wordtag in line:
            #print(words_and_tags[0],words_and_tags[1])
            w_t=(wordtag[0],wordtag[1])
            if w_t not in words_given_tags:
                words_given_tags[w_t]=1
            else:
                words_given_tags[w_t]+=1
    #print(words_given_tags)

    #caluculate the probabilty of word given tags = P(w|t)=p(w&t)/p(t)
    proability_words_given_tags={}
    for w_t in words_given_tags:
        proability_words_given_tags[w_t]=words_given_tags.get(w_t)/tag_dic.get(w_t[1])


    bigram_tag_dic={}
    #lets create the bigram model of the tags:
    for line in flines:
        line=preprocess(line)


        for i in range(len(line)-1):
            bigram_tag=(line[i+1][1],line[i][1])
            if bigram_tag not in bigram_tag_dic:
                bigram_tag_dic[bigram_tag]=1
            else:
                bigram_tag_dic[bigram_tag]+=1
    #print (bigram_tag_dic)

    probabilty_tag_given_tag={}

    for bigram_tag in bigram_tag_dic:
        #print(bigram_tag)
        #print(bigram_tag[1])
        probabilty_tag_given_tag[bigram_tag]=bigram_tag_dic.get(bigram_tag)/tag_dic.get(bigram_tag[1])



    return words_given_tags,proability_words_given_tags,probabilty_tag_given_tag


def readinputlines(filepath):
    f = open(filepath, "r")
    f = f.readlines()
    updatedlines=[]
    for line in f:
        new_line="<S>_<S> "+line+" </S>_</S>"
        updatedlines.append(new_line)
    return updatedlines


def pos_model(check_sentance,words_given_tags,proability_words_given_tags, probabilty_tag_given_tag):
    sentance = check_sentance.split()
    for i in range(0, len(sentance)):
        sentance[i] = sentance[i].split('_')

    #to find possible tags of the sentance
    keylist = list()
    for i in words_given_tags.keys():
        keylist.append(i)

    #dictionary of key and its possible tags
    key_tags_combinations={}
    i=1
    for word in sentance:
        taglist=[]
        for key in keylist:
            if(word[0]==key[0]):
                taglist.append(key[1])

        if(len(taglist)>0):
            key_tags_combinations[word[0]+" "+str(i)]=taglist
            i+=1
    print("---------------------------------------------------")
    print("words with the possible tags")
    print(key_tags_combinations)
    print("---------------------------------------------------")


    tag_tag_sequence=[]
    word_tag_order={}
    i=1
    for key in key_tags_combinations:
        keys=key.split()
        if(len(key_tags_combinations.get(key))==1):
            pair=(key,key_tags_combinations.get(key)[0])
            word_tag_order[i]=pair
            tag_tag_sequence.append(key_tags_combinations.get(key)[0])


        else:
            max_word_tag={}
            max_tag_tag={}
            previous_word=word_tag_order.get(i-1)
            #print(previous_word[0].split()[0])
            previous_word_possible_tags=key_tags_combinations.get(previous_word[0].split()[0]+" "+str(i-1))
            for tags in key_tags_combinations.get(key):
                pair=(keys[0],tags)
                pair1=(key,tags)
                max_word_tag[pair1]=proability_words_given_tags.get(pair)

            for tags in key_tags_combinations.get(key):
                for prevtags in previous_word_possible_tags:
                    pair=(tags,prevtags)
                    max_tag_tag[pair]=probabilty_tag_given_tag.get(pair)

            max_tag_value=0
            max_tag=()
            max_word=()
            for tag_tag in max_tag_tag:
                for word_tag in max_word_tag:
                    if((tag_tag[0]==word_tag[1]) and (max_word_tag.get(word_tag) is not None) and (max_tag_tag.get(tag_tag)is not None)):
                        #print(word_tag)
                        product=max_word_tag.get(word_tag)*max_tag_tag.get(tag_tag)
                        if(product>max_tag_value):
                            max_tag_value=product
                            max_tag=tag_tag
                            max_word=word_tag


            # print(tag_tag_sequence)
            # print(word_tag_order)
            tag_tag_sequence.append(max_tag[0])
            word_tag_order[i] = (max_word)
            # print(max_tag_tag)
            #print(max_word_tag)
            # print(max_tag)
            #print(max_word)
        i = i + 1

    word_tag_order.pop(1)
    word_tag_order.pop(len(word_tag_order)+1)



    word_tag_dic={}
    #create the word tag probabilities
    for key in word_tag_order.keys():
        pair=word_tag_order.get(key)
        pair=(pair[0].split()[0],pair[1])
        word_tag_dic[word_tag_order.get(key)]=proability_words_given_tags.get(pair)
    #create the bigrmas
    tag_tag_bigram_dic={}
    for i in range(len(tag_tag_sequence)-1):
        pair=(tag_tag_sequence[i+1],tag_tag_sequence[i])
        tag_tag_bigram_dic[pair]=probabilty_tag_given_tag.get(pair)

    print("the probabilities of the given tag sequence are and the best tag sequence is:")
    print (tag_tag_bigram_dic)
    print("------------------------------------------------------------------------------")
    print("the word tag probabilities are")
    print (word_tag_dic)


    total_probability=1


    for key in word_tag_dic:
        total_probability *= word_tag_dic.get(key)
    for key in tag_tag_bigram_dic:
        total_probability *= tag_tag_bigram_dic.get(key)

    print("---------------------------------------------------")
    print("the total probabilty after pos tagging is:")
    print(total_probability)
    print("----------------*********--------------------------")


if __name__ == "__main__":
    filepath = 'input.txt'
    f = readinput(filepath)
    flines=readinputlines(filepath)
    word_tag = preprocess(f)
    words_given_tags,proability_words_given_tags,probabilty_tag_given_tag=models(word_tag,flines)
    check_sentance=input("Enter a sentance:")
    check_sentance="<S> "+check_sentance+" </S>"
    pos_model(check_sentance,words_given_tags,proability_words_given_tags,probabilty_tag_given_tag)


