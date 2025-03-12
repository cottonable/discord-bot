import random

def cat_emoji():
    emojis = ["<:catsit:1347935719036944425>", 
              "<:goobercat:1347935688271859783>", 
              "<:cutey:1347935657107914761>", 
              "<a:catinsanity:1347935643841462355>", 
              "<a:catmindblown:1347935630809628734>", 
              "<a:cateat:1347935612715405365>", 
              "<:cat:1347935601143316511>", 
              "<:catburger:1347935586836545626>", 
              "<a:oiia:1347935566725120031>",
              "<:love4you:1347935546189545552>",
              "<:cat2:1347935532151210098>"
             ]
    random_emoji = random.choice(emojis)
    return random_emoji

def cat_fact():
    facts = [
        "the oldest known pet cat existed 9,500 years ago",
        "cats spend 70% of their lives sleeping, according to [Veterinary Hub](<https://veterinaryhub.com/cats-spend-70-of-their-lives-asleep/>)",
        "the richest cat in the world had £7 million",
        "a cat named Stubby was the mayor of an alaskan town for 20 years",
        "the record for the longest cat ever is 48.5 inches",
        "a cat went to space in 1963",
        "ancient egyptians would shave off their eyebrows when their cats died",
        "a house cat can reach speeds of up to 30mph",
        "the oldest cat in the world was 38 years old",
        "cats cannot taste sweets :(",
        "each cat's nose print is unique, like human fingerprints",
        "the loudest purr recorded was 67.8 dB"
        ]
    random_fact = random.choice(facts)
    return random_fact

def coinflip():
    side = ["<:heads:1348291871033659392> heads!!!! <:heads:1348291871033659392>",
            "<:tails:1348291883222438030> tails!!!! <:tails:1348291883222438030>"]
    random_side = random.choice(side)
    return random_side

def random_number(fromnr, tonr):
    fromnr = int(fromnr)
    tonr = int(tonr)
    result = random.randrange(fromnr, tonr + 1)
    print(result)
    return result